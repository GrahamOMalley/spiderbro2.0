import configuration
import DAL
import piratebaysearcher
import formatting
from pytvdbapi import api
from datetime import date
import logging as log

class spider:
    """ class that finds torrents for missing episodes of shows"""

    def __init__(self, dal=DAL.DAL()):
        self.config = configuration.get_args()
        self.dal = dal

    def get_tvdb_episodes(self, show, date_to_check=date.today()):
        """
        return a dictionary of {int: list} respresenting a tv shows seasons and episodes
        """
        episodes_in_tvdb = {}
        status = "Error?"
        try:
            thetvdb = api.TVDB('046CE679C95B0D0C')
            result = thetvdb.search(show, 'en')
            tvdbshow = result[0]
            num_seasons = len(tvdbshow)
            status = tvdbshow.Status
            
            for season in tvdbshow.seasons.keys():
                episodes_in_tvdb[season] = []
                for episode in tvdbshow.seasons[season].episodes:
                    aired = tvdbshow.seasons[season][episode].FirstAired
                    if(aired != '' and aired < date_to_check):
                        episodes_in_tvdb[season].append(episode)
        except Exception as e:
            log.error(e)

        if status == "Ended":
            self.dal.mark_show_ended(show)

        if 0 in episodes_in_tvdb: episodes_in_tvdb.pop(0)
        return episodes_in_tvdb, status

    def get_missing_episodes(self, show):
        """
        returns a list of 
        """
        self.dal.update_show_table(show)
        missing_episodes = {}

        episodes_in_tvdb, status = self.get_tvdb_episodes(show)
        episodes_in_library = self.dal.get_eps_for_show(show)

        for season, episodes in episodes_in_tvdb.items():
            if season not in episodes_in_library:
                if season != max(episodes_in_tvdb) or status == 'Ended':
                    missing_episodes[season] = [-1]
                    continue
                else:
                    episodes_in_library[season] = []
            for episode in episodes:
                if episode not in episodes_in_library[season]:
                    if season not in missing_episodes: missing_episodes[season] = []
                    missing_episodes[season].append(episode)

        return missing_episodes

    def find_torrents_for_show(self, show):
        log.info("Looking for episodes for %s" % show)
        missing = self.get_missing_episodes(show)
        if missing:
            for season, episodes in missing.items():
                for episode in episodes:
                    log.info("\tLooking for s%se%s" % (season, episode))
                    # TODO: support multiple torrent searchers/factory/prototype pattern
                    pirate = piratebaysearcher.piratebaysearcher()
                    torrent = pirate.find_torrent(show, season, episode)
                    if torrent != None:
                        log.info("Found torrent: %s" % (torrent))
                        save_path = self.get_save_path(show, season, episode)
                        self.dal.mark_episode_for_download(show, season, episode, torrent, save_path)
        else:
            log.info("\t%s is up to date" % show)

    def get_save_path(self, show, season, episode):
        return self.config.save_dir + show.replace(" ", "_") + "_s" + formatting.format_number(season) + "e" + formatting.format_number(episode)
        