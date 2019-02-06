import logging
from datamodel.search.Cwpark2HawonsYeonjh_datamodel import Cwpark2HawonsYeonjhLink, OneCwpark2HawonsYeonjhUnProcessedLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(Cwpark2HawonsYeonjhLink)
@GetterSetter(OneCwpark2HawonsYeonjhUnProcessedLink)
class CrawlerFrame(IApplication):
    app_id = "Cwpark2HawonsYeonjh"

    def __init__(self, frame):
        self.app_id = "Cwpark2HawonsYeonjh"
        self.frame = frame


    def initialize(self):
        self.count = 0
        links = self.frame.get_new(OneCwpark2HawonsYeonjhUnProcessedLink)
        if len(links) > 0:
            print "Resuming from the previous state."
            self.download_links(links)
        else:
            l = Cwpark2HawonsYeonjhLink("http://www.ics.uci.edu/")
            print l.full_url
            self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get_new(OneCwpark2HawonsYeonjhUnProcessedLink)
        if unprocessed_links:
            self.download_links(unprocessed_links)

    def download_links(self, unprocessed_links):
        for link in unprocessed_links:
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(Cwpark2HawonsYeonjhLink(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
'''
rawDataObj is an object of type UrlResponse declared at L20-30
datamodel/search/server_datamodel.py
the return of this function should be a list of urls in their absolute form
Validation of link via is_valid function is done later (see line 42).
It is not required to remove duplicates that have already been downloaded. 
The frontier takes care of that.

Suggested library: lxml
'''
def extract_next_links(rawDataObj):
	outputLinks = []
	dom = html.fromstring(rawDataObj.content) # convert the html content of webpage to HtmlElement obj
	urls = dom.xpath('//a/@href') # returns list of paths
	
	for link in urls:
		try:
			# print '###############'
			# print link
			outputLinks.append(link)
		except:
			pass
	return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False

