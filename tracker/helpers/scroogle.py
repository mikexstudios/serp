from django.conf import settings

import urllib, urllib2
from BeautifulSoup import BeautifulSoup

class Scroogle():
    '''
    Uses http://scroogle.org to obtain search results.
    '''
    api_url = 'http://www.scroogle.org/cgi-bin/nbbw.cgi'
    query = '' #our query (the Gw param)
    n = 1 #2 = 20 results; 5 = 50 results; 1 = 100 results
    
    def __init__(self):
        pass

    def search(self, query):
        self.query = query

        #Construct the query params
        params = {
            'Gw': self.query,
            'n': self.n,
        }

        #Now make the query
        query_params = urllib.urlencode(params)
        url = '%s?%s' % (self.api_url, query_params)
        #NOTE: We keep response as a file-like object so that soup can load it
        #      efficiently.
        self.response = urllib2.urlopen(url)

        #Parse the response
        self.__process_response()
        
        return self.results
    
    def __process_response(self):
        #We put our results as a list of dicts.
        self.results = []

        #Parse the HTML
        soup = BeautifulSoup(self.response)

        #Scroogle has a <ul> for each search result
        uls = soup.findAll('ul')
        for i, ul in enumerate(uls):
            result = {}
            #Not really necessary to have the rank since the list is ordered by
            #ranking, but this may be helpful
            result['rank'] = i

            a = ul.previousSibling.previousSibling
            result['url'] = a['href']

            #Each title sometimes has the searched keyword wrapped in <b>. We
            #strip all HTML tags from the title.
            result['title'] = ''.join(a.findAll(text = True))

            #The last piece of text in the ul is the URL again, so we grab all
            #elements of the returned list except the last element.
            result['content'] = ''.join(ul.findAll(text = True)[:-1])

            self.results.append(result)

        #Pull out some important parts of the response
        self.result_count = len(uls)
