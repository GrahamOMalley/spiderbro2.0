import re
import formatting
import logging as log
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

class piratebaysearcher:
    """ searches tpb for a torrent """

    def __init__(self):
        self.site_url = self.get_a_valid_proxy()

    def get_a_valid_proxy(self):
        #TODO: need a static class or somesuch that tests all piratebay proxies when program starts and gets the first working one
        return "https://theproxypirate.pw"
        #return "https://pirateproxy.sx/"

    def find_torrent(self, showname, season, episode):
        """
        searches piratebay for a torrent
        """
        show = self.normalise_show_name(showname)
        proxy = self.get_a_valid_proxy()
        if(proxy == None):
            raise ValueError("Unable to find working piratebay proxy")

        for season_episode_string in self.get_torrent_search_strings(season, episode):
            search_url = quote("/search/" + show + " " + season_episode_string)
            search_url = self.site_url + search_url
            log.info("\t\tTrying search url: %s" % search_url)
            try:
                resp = urlopen(search_url)
                page = resp.read()
                soup = BeautifulSoup(page)
                links = soup.findAll('a', href=re.compile( "^magnet"))
                for link in links:
                    if self.validate_link(show, link['href'], season_episode_string):
                        return link['href']
            except Exception as e:
                log.error("Piratebaysearch encountered an error trying to open a page:")
                log.error(e)

        return None

    def normalise_show_name(self, name):
        """
        strips out characters that might interfere with getting a clean search result
        """
        # remove characters we don't want in the name
        replace_chars =";:@#-!,/" 
        strip_chars ="'()" 

        for char in replace_chars:
            name = name.replace(char, " ")

        for char in strip_chars:
            name = name.replace(char, "")

        # get rid of extra whitespace
        name = ' '.join(name.split())

        # TODO: should follow old logic and try multiple strings with & and 'and'
        name = name.replace('&', 'and')

        return name
        
    def validate_link(self, show, link, season_episode_string):
        """
        retuns true or false based on whether a magnet link meets validation criteria
        """
        # First validate the link title is ok
        log.debug('\t\tValidating %s' % (formatting.get_torrent_name_from_magnet(link)))
            
        delimiters = [".", "+"]
        for delimiter in delimiters:
            link_show_expression = delimiter.join(show.split(" "))
            season_episode_expression = delimiter.join(season_episode_string.split(" "))
            if link_show_expression.lower() in link.lower() and season_episode_expression.lower() in link.lower():
                log.debug("%s and %s found in link, passing validation")
                return True

        return False

    def get_torrent_search_strings(self, season, episode):
        """
        returns several different season/episode/series patterns to search for
        """
        search_strings = []

        if episode == -1:
            search_expressions = ["season %s", "series %s"]
            for expression in search_expressions:
                search_strings.append(expression % (season))
        else:
            search_expressions = ["s%se%s"]
            for expression in search_expressions:
                search_strings.append(expression % (formatting.format_number(season), formatting.format_number(episode)))

        return search_strings
        
