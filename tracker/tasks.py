from django.conf import settings

#from celery.decorators import task
from celery.task import Task, PeriodicTask

from .models import Track, Check
#from .helpers import 
from .helpers.googlesearch import GoogleSearch
from .helpers.scroogle import Scroogle
from .helpers import pagerank

import os
import urllib #for urlopen
import time, random #for sleep
from datetime import datetime, timedelta #for PeriodicTask
#import re #for regex matching url
#import urlparse #getting domain part of url
from fnmatch import fnmatch #for wildcards in url matching

class ExampleTask(Task):
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)

        logger.info('Executed example task')
        return True
#Don't really need this because of autodiscovery:
#tasks.register(ExampleTask)

class CheckRankingTask(Task):
    #By default, we run this task in the low priority queue unless overridden.
    routing_key = 'low'
    #Sometimes, there might be some issue, and so we don't want this task to keep
    #hitting the search provider.
    default_retry_delay = 30 * 60 #30 minutes
    max_retries = 1
    rate_limit = settings.CHECK_RATE_LIMIT

    def run(self, track_id, check_id = None, ip_address = '127.0.0.1', **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info('Using IP Address: %s' % ip_address)
        
        #Get Track obj
        t = Track.objects.get(id = track_id)
        logger.info('Keywords: %s' % t.keyword)
        logger.info('Url: %s' % t.url)

        #If a check_id is passed in, then we use that existing Check obj instead
        #of creating a new one.
        if check_id:
            c = Check.objects.get(id = check_id)
            c.track = t
        else:
            #Create a new Check
            c = Check()
            c.track = t
            #is_done flag defaults to False
            c.save()

        def url_compare(result_url):
            #We only rstrip result_url if t.url ends in '/' too.
            if t.url[-1] == '/':
                return fnmatch(result_url.rstrip('/'), t.url.rstrip('/'))
            return fnmatch(result_url, t.url)
        
        if settings.SEARCH_METHOD == 'scroogle':
            #We need to keep track of the matched url since in wildcard URL cases,
            #we can't get pagerank on a wildcard URL. So we get PR on the matched
            #url.
            matched_url = False
            s = Scroogle()
            results = s.search(t.keyword)
            for i, r in enumerate(results):
                if url_compare(r['url']):
                    #We found the url!
                    c.position = i + 1 #since i starts at 0, but pos starts at 1.
                    matched_url = r['url']
                    break

            if matched_url:
                #Get pagerank
                c.pagerank = int(pagerank.get_pagerank(matched_url))
                logger.info('Got pagerank: %s' % c.pagerank)
        
        #TODO: Port "regex" matching for google ajax api too.
        elif settings.SEARCH_METHOD == 'google':
            #Set up Google Searching
            g = GoogleSearch(settings.GOOGLE_AJAX_API_KEY)
            g.userip = ip_address
            g.referrer = 'http://%s/' % g.userip
            #We want to search for this:
            g.q = t.keyword
            
            #Helper function for processing results:
            def results_match_url(results):
                for i, r in enumerate(results):
                    if url_compare(r['unescapedUrl']):
                        #We found the url!
                        return i+1 #start at 1
                return False
            
            #Now we search and process results at the same time.
            results_offset = 0
            for results in g:
                rmu = results_match_url(results)
                if rmu:
                    #Great! We found a match in the results.
                    c.position = results_offset + rmu
                    break
                #Otherwise, continue until we run out of result sets. Since we
                #have our offset be at 0, we need to make adding results also be
                #0-indexed.
                results_offset += len(results)

                #So we don't get banned by Google, let's sleep for a bit.
                time.sleep(random.randint(5, 15)) #sec
                logger.info('Not in the first %s results. Getting more...' % results_offset)

            logger.info('all done!')

            #Get pagerank
            c.pagerank = int(pagerank.get_pagerank(t.url))
            logger.info('Got pagerank: %s' % c.pagerank)
        else:
            logger.info('Using dummy results!')
            time.sleep(10)
            c.position = random.randint(1, settings.MAX_SEARCH_RESULTS)
            if '*' not in t.url:
                c.pagerank = random.randint(0, 5)
        
        #TODO: Check to see if task was deleted. We delete tasks when we want to
        #      expire them.
        c.is_done = True
        c.save()
        
        #Update Track to set the time of last_checked
        t.last_checked = c.created
        t.save()
        
        #Report on what we found
        if c.position is None:
            logger.info('Not ranked in the first %s results!' % settings.MAX_SEARCH_RESULTS)
        else:
            logger.info('Ranked in position: %s' % c.position)
        
        if c.position is None:
            #Fixes column result null problem
            return True
        return c.position

class InstantCheckRankingTask(CheckRankingTask):
    '''
    We use this when we want to run the Check task immediately.
    '''
    routing_key = 'high'
    rate_limit = '6/m' #roughly 10 sec per task.

class TrackPeriodicTask(PeriodicTask):
    routing_key = 'high' #by default, use high priority
    #We want to run this every < 1 hr since our cloud servers get charged every
    #hour, not prorated.
    run_every = timedelta(minutes = 50)
    #run_every = timedelta(minutes = 3)
    #run_every = timedelta(seconds = 15)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)

        logger.info('Running periodic task!')

        #TODO: Kill any existing servers.

        #Get tracks that haven't been updated today (before 0:00 today). First,
        #we need to set up the earliest bound for "today".
        now = datetime.now()
        today_start = datetime(now.year, now.month, now.day) #everything else is 0

        #Make the selection. We take the first 1000 since we want to try to fit it
        #into what one server can do in one hour.
        tracks = Track.objects.filter(is_active = True, 
                                      last_checked__lt = today_start)[:1000]
        logger.info('Got %s Track obj that have not been updated today.' % tracks.count())

        #Start the server.
            
        for t in tracks:
            logger.info('Running check for Track: %s' % t.id)
            CheckRankingTask.delay(t.id)

        return True

class TestRateTask(Task):
    #By default, we run this task in the low priority queue unless overridden.
    routing_key = 'low'
    #According to my testing, the rate limiter will space the tasks apart and will
    #not bunch them all together => creating uniformity and predictable runtimes.
    rate_limit = '3/m'

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info('Exec Test task!')

        return True

