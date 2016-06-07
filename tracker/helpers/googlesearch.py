from django.conf import settings

import urllib, urllib2
import time, random #for sleep
try:
    import json
except ImportError:
    import simplejson as json

class GoogleSearch():
    '''
    See: http://code.google.com/apis/ajaxsearch/documentation/reference.html#_intro_fonje
    '''
    api_url = 'http://ajax.googleapis.com/ajax/services/search/web'
    q = ''
    v = '1.0'
    userip = ''
    rsz = 'large'
    referrer = ''
    
    #Keeps track of the current page of search results that we are on.
    page_index = None

    def __init__(self, key = ''):
        self.key = key

    def search(self, query, extra_params = {}):
        self.q = query
        #Construct the query params
        #TODO: We need some way that if the key has None value, we don't include it.
        #      Because if we don't specify a key, it's breaking the search.
        params = {
            'q': self.q,
            'v': self.v,
            'userip': self.userip,
            'rsz': self.rsz,
            'key': self.key,
        }
        #Add the extra params dict to the params dict.
        params.update(extra_params)
        
        #Now make the query
        query_params = urllib.urlencode(params)
        url = '%s?%s' % (self.api_url, query_params)
        request = urllib2.Request(url, None, {'Referer': self.referrer})
        self.response = urllib2.urlopen(request)
        self.response = self.response.read() #get everything from file obj

        #Parse the response
        self.__process_response()
        
        return self.results
    
    def __process_response(self):
        #Parse the json
        self.response = json.loads(self.response)

        #Pull out some important parts of the response
        self.result_count = self.response['responseData']['cursor']['estimatedResultCount']
        self.results = self.response['responseData']['results']
        
        #Starts at 0.
        self.page_index = self.response['responseData']['cursor']['currentPageIndex']
        #The pages array always remains constant. We technically don't need to 
        #refresh it every time.
        self.pages = self.response['responseData']['cursor']['pages']

    def __iter__(self):
        return self

    def next(self):
        '''
        Returns the next page of search results.
        '''
        if self.page_index == None:
            #Initial case, we search without specifying where to start.
            return self.search(self.q)
        
        try:
            p = self.pages[self.page_index + 1] #Try to get next page.
        except IndexError:
            raise StopIteration

        #Search for the same query, but start the results on the next page.
        p['start'] = int(p['start'])
        return self.search(self.q, {'start': p['start']})

    def get_all_results(self, wait = True):
        cumulative_results = []
        for r in self:
            #Add result to the cumulative_results
            cumulative_results.extend(r)
            
            #So we don't get banned by Google, let's sleep for a bit.
            time.sleep(random.randint(5, 15)) #sec
        
        return cumulative_results
