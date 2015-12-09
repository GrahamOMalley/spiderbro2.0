import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from urllib.request import urlopen
import piratebaysearcher

class Test_piratebay(unittest.TestCase):
    def test_can_open_pirate_bay(self):
        resp = urlopen('https://theproxypirate.pw/search/arrow/0/7/')
        self.assertEqual('OK', resp.msg)

    # this is more of an integration test - since we're testing a volatile resource most of these sort of will be though
    def test_can_get_a_valid_proxy(self):
        pirate = piratebaysearcher.piratebaysearcher()
        proxy = pirate.get_a_valid_proxy()
        self.assertIsNotNone(proxy)

    def test_throws_exception_if_no_proxy_available(self):
        pirate = piratebaysearcher.piratebaysearcher()
        pirate.get_a_valid_proxy = MagicMock(return_value = None)
        with self.assertRaises(ValueError):
            torrent = pirate.find_torrent("Grey's Anatomy", 1, 11)
    
    def test_can_normalise_search_terms(self):
        shows = { 
            "Adam And Joe Go Tokyo":"Adam And Joe Go Tokyo",
            "American Dad!":"American Dad",
            "Archer (2009)":"Archer 2009",
            "Avatar: The Last Airbender":"Avatar The Last Airbender",
            "Berry & Fulcher's Snuff Box":"Berry and Fulchers Snuff Box",
            "Lucy, The Daughter of the Devil":"Lucy The Daughter of the Devil",
            "Penn & Teller: Bullshit!":"Penn and Teller Bullshit",
            "Star Wars - The Clone Wars":"Star Wars The Clone Wars",
            "Don't Trust the B---- In Apartment 23":"Dont Trust the B In Apartment 23",
            "NTSF:SD:SUV::":"NTSF SD SUV",
            "Steins;Gate":"Steins Gate",
            "Love/Hate":"Love Hate"
        }
        pirate = piratebaysearcher.piratebaysearcher()
        for k,v in shows.items():
            self.assertEqual(pirate.normalise_show_name(k), v)

    def test_validate_link_passes_basic_check(self):
        pirate = piratebaysearcher.piratebaysearcher()
        is_ok = pirate.validate_link("Greys Anatomy", "magnet:?xt=urn:btih:9a3e3907f4282a033746c971a5ec2fdaab78e097&dn=Greys.Anatomy.S11E23.HDTV.x264-LOL%5Bettv%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.com%3A6969", "s11e23")
        self.assertTrue(is_ok)

    def test_can_get_torrent_for_single_episode_with_standard_url_scheme(self):
        # TODO: this test must be more specific. this test must mock the page response.
        pirate = piratebaysearcher.piratebaysearcher()
        magnet = pirate.find_torrent("Grey's Anatomy", 11, 23)
        self.maxDiff=None
        self.assertEqual("magnet:?xt=urn:btih:9a3e3907f4282a033746c971a5ec2fdaab78e097&dn=Greys.Anatomy.S11E23.HDTV.x264-LOL%5Bettv%5D&tr=udp%3A//tracker.openbittorrent.com%3A80&tr=udp%3A//open.demonii.com%3A1337&tr=udp%3A//tracker.coppersurfer.tk%3A6969&tr=udp%3A//exodus.desync.com%3A6969", magnet)


    def test_can_get_torrent_for_whole_season(self):
        pirate = piratebaysearcher.piratebaysearcher()
        magnet = pirate.find_torrent("Luther", 2, -1)
        self.maxDiff=None
        self.assertEqual("magnet:?xt=urn:btih:f95619bd0eee3236dffd950bc635e3a485dbdf75&dn=Luther+Season+2+Complete+HDTV+XviD-soupuciaTPB&tr=udp%3A//tracker.openbittorrent.com%3A80&tr=udp%3A//open.demonii.com%3A1337&tr=udp%3A//tracker.coppersurfer.tk%3A6969&tr=udp%3A//exodus.desync.com%3A6969", magnet)

        # test to figure out why '&' isn't getting correctly replaced in Key & Peele
# TODO
        # test can deal with alternative url patterns and magnet link delimiters
        # example: "Marvels Agents Of S.H.I.E.L.D." changes the search url because of the '.'s

        # test can identify high quality
        # test can identify low quality


if __name__ == '__main__':
    unittest.main()
