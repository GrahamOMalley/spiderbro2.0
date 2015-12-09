# python 3 compatibility
import configuration
import DAL
import logging as log
import spider

configuration.setup_logging()
log.info("SpiderBro, two point oh!")

dal = DAL.DAL()
sbro = spider.spider(dal)

# TODO: implement cmdline args for 1 show, all shows, all shows airing this week

for show in dal.get_full_show_list():
    ga_list = sbro.find_torrents_for_show(show)