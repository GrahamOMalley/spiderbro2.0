# python 3 compatibility
import configuration
import DAL
import logging as log

configuration.setup_logging()
log.info("SpiderBro, two point oh!")
dal = DAL.DAL()