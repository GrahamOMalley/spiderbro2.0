import unittest
import spider
import DAL
from unittest.mock import Mock
from unittest.mock import MagicMock
from datetime import date

class Test_spider(unittest.TestCase):

    def test_can_get_missing_episodes(self):
        mockDAL = Mock(spec=DAL.DAL)
        mockDAL.get_eps_for_show = MagicMock(return_value = {1: [1, 2]})
        spiderbro = spider.spider(mockDAL)
        missing_episodes = spiderbro.get_missing_episodes("Life On Mars")
        self.assertDictEqual(missing_episodes, {1:[3,4,5,6,7,8], 2:[-1]})

    def test_can_get_tvdbshow_episode_list(self):
        spiderbro = spider.spider()
        tvdb_episodes, status = spiderbro.get_tvdb_episodes('Life On Mars')
        self.assertDictEqual(tvdb_episodes, {1:[1,2,3,4,5,6,7,8], 2:[1,2,3,4,5,6,7,8]})
    
    def test_gets_only_aired_eps(self):
        spiderbro = spider.spider()
        mockdate = date(2015, 1, 20) # only season ep 9 has aired at this point
        tvdb_episodes, status = spiderbro.get_tvdb_episodes('Constantine', mockdate)
        self.assertDictEqual(tvdb_episodes, {1:[1,2,3,4,5,6,7,8,9]})

    def test_ignores_specials(self):
        spiderbro = spider.spider()
        tvdb_episodes = spiderbro.get_tvdb_episodes('Doctor Who (2005)')
        self.assertNotIn(0, tvdb_episodes)

    def test_dont_mark_download_whole_season_if_season_not_finished_airing(self):
        mockDAL = Mock(spec=DAL.DAL)
        mockDAL.get_eps_for_show = MagicMock(return_value = {})
        spiderbro = spider.spider(mockDAL)
        tvdb_episodes = spiderbro.get_missing_episodes('Orphan Black')
        self.assertNotEqual(tvdb_episodes[3], [-1])

    def test_mark_show_as_ended(self):
        mockDAL = Mock(spec=DAL.DAL)
        spiderbro = spider.spider(mockDAL)
        tvdb_episodes, status = spiderbro.get_tvdb_episodes('Life On Mars')
        mockDAL.mark_show_ended.assert_called_with('Life On Mars')

    def test_updates_show_table(self):
        mockDAL = Mock(spec=DAL.DAL)
        mockDAL.get_eps_for_show = MagicMock(return_value = {1: [1, 2]})
        spiderbro = spider.spider(mockDAL)
        missing_episodes = spiderbro.get_missing_episodes("Life On Mars")
        mockDAL.update_show_table.assert_called_with('Life On Mars')

    def test_saves_successful_search_in_database(self):
        mockDAL = Mock(spec=DAL.DAL)
        mockDAL.get_eps_for_show = MagicMock(return_value = {1: [1,2,3,4,5,6,7,8,9,10,11,12]})
        spiderbro = spider.spider(mockDAL)
        spiderbro.find_torrents_for_show("Constantine")
        mockDAL.mark_episode_for_download.assert_called_once_with("Constantine", 1, 13, unittest.mock.ANY, unittest.mock.ANY)

        #TODO:
        # test that we can mark episodes as 'given up' when a switch enabling this behaviour is passed in and no torrent is found
    def test_marks_episode_as_do_not_download(self):
        mockDAL = Mock(spec=DAL.DAL)
        mockDAL.get_eps_for_show = MagicMock(return_value = {1: [1,2,3,4,5,6,7,8,9,10,11,12]})
        spiderbro = spider.spider(mockDAL)
        spiderbro.config.force_learn = True
        spiderbro.find_torrents_for_show("Constantine")
        mockDAL.mark_episode_do_not_download.assert_called_once_with("Constantine", 1, 13, unittest.mock.ANY, unittest.mock.ANY)

if __name__ == '__main__':
    unittest.main()
