#! /usr/bin/env python
import MySQLdb
import sys
import logging as log
import configuration

class DAL:

    def __init__(self):
        self.config = configuration.get_args()
        
        try:
            # test connection, throw error if not valid
            con = self.get_connection()
            con.close()
            log.debug("Connected to db OK")
        except:
            log.fatal("Database connection is invalid, application exiting...")
            #sys.exit()
        
        # connectin is good, setup tables if they don't exist        
        self.check_or_create_additional_tables()

    def get_connection(self):
        """
        Use the host/user/pwd/schema settings to acquire a db connection
        """
        con = MySQLdb.connect(self.config.host, self.config.user, self.config.pwd, self.config.kodi_schema)
        return con

    def check_or_create_additional_tables(self):
        """
        Create the torrents table in the Kodi db if it doesn't already exist
        """
        con = self.get_connection()
        create_torrents_table_cmd="""CREATE TABLE IF NOT EXISTS `spiderbro_torrents` ( `showname` VARCHAR(200) NOT NULL, `season` int(11) DEFAULT NULL, `episode` int(11) DEFAULT NULL, `url` VARCHAR(2000), `status` varchar(10) , `savepath` VARCHAR(2000), PRIMARY KEY (showname, season, episode)) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
        try:
            cursor = con.cursor()
            # suppress warning about table existing already
            cursor.execute("SET sql_notes = 0; ")
            cursor.execute(create_torrents_table_cmd)
            cursor.execute("SET sql_notes = 1; ")
            cursor.close()
        except Exception as e:
            log.error(e)

        create_shows_table_cmd="""CREATE TABLE IF NOT EXISTS `spiderbro_shows` ( `showname` VARCHAR(200) NOT NULL UNIQUE, `high_quality` tinyint(1) NOT NULL DEFAULT '0', `finished` tinyint(1) NOT NULL DEFAULT '0') ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        try:
            cursor = con.cursor()
            # suppress warning about table existing already
            cursor.execute("SET sql_notes = 0; ")
            cursor.execute(create_shows_table_cmd)
            cursor.execute("SET sql_notes = 1; ")
            cursor.close()
            con.close()
        except Exception as e:
            log.error(e)

    def get_full_show_list(self):
        """
        Return a list of every show from the kodi database
        """
        all_shows = []
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("select c00 from tvshow where c00 not in (select showname from spiderbro_shows where finished=1) order by c00;")
            for c in cursor:
                all_shows.append(c[0])

            cursor.close()
            con.close()
            return all_shows
        except Exception as e:
            log.error(e)

    def get_eps_for_show(self, show):
        """
        Return a dict of {season: [episodes]} for a show
        """
        episodes = {}
        con = self.get_connection()
        try:
            cursor = con.cursor()
            # TODO: filter on status != DONT_DOWNLOAD
            cursor.execute("""select c12, c13 from episode_view where strTitle = \"%s\" UNION select season, episode from spiderbro_torrents where showname=\"%s\" and STATUS != 'DONT_DOWNLOAD' """ % (show, show))
            for c in cursor:
                season = int(c[0])
                if season not in episodes: episodes[season] = [] 
                episodes[season].append(int(c[1]))

            cursor.close()
            con.close()

        except Exception as e:
            log.error(e)

        return episodes

    def mark_show_ended(self, show):
        """
        marks a show as finished
        """
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""update spiderbro_shows set finished=1 where showname=\"%s\" """ % show)
            cursor.close()
            con.commit()
            con.close()
        except Exception as e:
            log.error(e)

    def update_show_table(self, show):
        """
        sets up inital show info if not present
        """
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""INSERT ignore into spiderbro_shows (showname) VALUE (\"%s\")""" % show)
            cursor.close()
            con.commit()
            con.close()
        except Exception as e:
            log.error(e)

    def mark_episode_for_download(self, show, season, episode, url, save_path):
        """
        marks an episode to be downloaded
        """
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""insert into spiderbro_torrents(showname, season, episode, url, status, savepath) values (\"%s\", \"%s\", \"%s\", \"%s\",'DOWNLOAD', \"%s\" ) ON DUPLICATE KEY UPDATE status='DOWNLOAD', url=\"%s\";""" % (show, season, episode, url, save_path, url))
            cursor.close()
            con.commit()
            con.close()
        except Exception as e:
            log.error(e)

    def get_pending_downloads(self):
        """
        Return a dict of {torrent: savepath}
        """
        downloads = {}
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""select showname, season, episode, url, savepath from spiderbro_torrents where status='DOWNLOAD'""")
            for c in cursor:
                showname = c[0]
                season = int(c[1])
                episode = int(c[2])
                url = c[3]
                savepath = c[4]
                downloads[savepath] = [showname, season, episode, url]

            cursor.close()
            con.close()

        except Exception as e:
            log.error(e)

        return downloads

    def mark_episode_download_successful(self, show, season, episode):
        """
        marks an episode SUCCESS
        """
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""update spiderbro_torrents set status="SUCCESS" where showname=\"%s\" and season=%d and episode=%d;""" % (show, season, episode))
            cursor.close()
            con.commit()
            con.close()
        except Exception as e:
            log.error(e)

    def mark_episode_do_not_download(self, show, season, episode):
        """
        marks an episode DONT_DOWNLOAD
        """
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""update spiderbro_torrents set status="DONT_DOWNLOAD" where showname=\"%s\" and season=%d and episode=%d;""" % (show, season, episode))
            cursor.close()
            con.commit()
            con.close()
        except Exception as e:
            log.error(e)

    def get_savepath_information(self, savepath):
        """
        Return a dict of {torrent: savepath}
        """
        savepath_information = {}
        con = self.get_connection()
        try:
            cursor = con.cursor()
            cursor.execute("""select showname, season, episode from spiderbro_torrents where savepath=\"%s\" """ % (savepath))
            for c in cursor:
                showname = c[0]
                season = int(c[1])
                episode = int(c[2])
                savepath_information[savepath] = [showname, season, episode]

            cursor.close()
            con.close()

        except Exception as e:
            log.error(e)

        return savepath_information