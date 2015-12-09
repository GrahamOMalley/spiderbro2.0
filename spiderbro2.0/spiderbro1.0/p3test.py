#! /usr/bin/env python
#from sb_utils import *
import sys
import urllib.request
import ssl

if __name__ == "__main__":
    """
        quick little testing script to see behaviour of search classes and test individual episodes/seasons
    """
#    e_masks = [NxN, sNeN, NNN]
#    s_masks = [season, series]
#    search_list = [piratebaysearch, btjunkiesearch, isohuntsearch]
#    tags = ["SWESUB", "SPANISH"]
#    opts = {"use_debug_logging":True, "log_dir":"log"}

    #log = get_sb_log(opts)

    #base = base_search()
    #base.search("Game of Thrones", "1", "3", sNeN, tags, True)
    
    #p = piratebaysearch()
    #result = p.search("Girls", "2", "2", sNeN, tags, True)
    #if result: log.info("\t\tFound Torrent: %s" % result)

    #i = isohuntsearch()
    #result = i.search("The Office (US)", "8", "17", sNeN, tags, False)
    #print e.search_url
    #if result: log.info("\t\tFound Torrent: %s" % result)
    
    #e = extratorrentsearch()
    #result = e.search("The Office (US)", "8", "17", sNeN, tags, False)
    #print e.search_url #if result: log.info("\t\tFound Torrent: %s" % result)

    #proxy_support = urllib.ProxyHandler({})
    #opener = urllib.build_opener(proxy_support)
    #urllib.install_opener(opener)
    #response = urllib.urlopen("http://extratorrent.cc/search/?search=downton+abbey&new=1&x=0&y=0")
    #request = urllib.request.urlopen("https://tpbproxy.co/search/Adventure+Time+s06e34/0/7/0")
    #request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    #request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0")
    #request.add_header('Accept-Language', "en-US,en;q=0.5")
    #response = urllib2.urlopen(request)
    #search_page = response.read()
    #print(search_page)

    from urllib.request import urlopen
    resp = urlopen('https://theproxypirate.pw/search/arrow/0/7/')
    print(resp.read())
