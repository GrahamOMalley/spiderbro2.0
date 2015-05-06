#! /usr/bin/env python
# python 3 compatibility
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import argparse
import os
import logging
from datetime import date
from datetime import datetime

def get_args():
    """
        read the configuration file, set opts
    """

    # Set up config file
    conf_parser = argparse.ArgumentParser(add_help=False)
    conf_parser.add_argument("--conf_file", help="Specify config file", metavar="FILE", default="config.ini")
    args, remaining_argv = conf_parser.parse_known_args()
    defaults = {"tv_dir" : "some default",}
    if args.conf_file:
        config = configparser.SafeConfigParser()
        config.read([args.conf_file])
        defaults = dict(config.items("spiderbro"))

    # Don't surpress add_help here so it will handle -h
    parser = argparse.ArgumentParser(parents=[conf_parser], formatter_class=argparse.RawDescriptionHelpFormatter, description='Spiderbro! Spiderbro! Finding episodes for your shows!')
    parser.add_argument('--test',  action="store_true", default=False, help='Don\'t actually download episodes')
    parser.add_argument('--debug_logging',  action="store_true", default=False, help='Turn on Debug Logging')

    parser.add_argument('--host', type=str, required=False, default="", help='Mysql host')
    parser.add_argument('--user', type=str, required=False, default="", help='Mysql user')
    parser.add_argument('--pwd', type=str, required=False, default="", help='Mysql password')
    parser.add_argument('--kodi_schema', type=str, required=False, default="", help='Kodi schema')
    parser.add_argument('--schema', type=str, required=False, default="", help='spiderbro schema')

    parser.add_argument('-a', '--all',  action="store_true", default=True, help='Find episodes for all shows')
    parser.add_argument('-cc', '--clear_cache',  action="store_true", default=False, help='Clear the SB episode cache for show(s)')
    parser.add_argument('-f', '--use_file_renamer',  action="store_true", default=True, help='Use the file_renamer script after torrent downloads')
    parser.add_argument('-hq', '--high_quality',  action="store_true", default=False, help='Switch show to high quality')
    parser.add_argument('-lq', '--low_quality',  action="store_true", default=False, help='Switch show to low quality')
    parser.add_argument('-l', '--force_learn',  action="store_true", default=False, help='Force SB to mark episode(s) as DONT_DOWNLOAD')
    parser.add_argument('-p', '--polite',  action="store_true", default=False, help='Wait N seconds before opening each url')
    parser.add_argument('-pv', '--polite-value', type=int, required=False, default=5, help='Num seconds for polite')
    parser.add_argument('-v', '--verbose',  action="store_true", default=False, help='Verbose output')

    parser.add_argument('-ld', '--log_dir', type=str, required=False, default="log", help='Logging Dir')
    parser.add_argument('-s', '--show', type=str, required=False, help='Find episodes for a single show')
    parser.add_argument('-t', '--tv_dir', type=str, required=False, default='/home/gom/nas/tv/', help='TV directory')
    parser.add_argument('--force_id', type=str, required=False, help='Force a show to change its id')

    parser.set_defaults(**defaults)
    args = parser.parse_args(remaining_argv)
    if args.show: args.all = False
    return args

def setup_logging():
    """
    Set up all the logging parameters for SpiderBro
    """

    start_day = str(datetime.today()).split(" ")[0]
    logfilename ='log' + os.path.sep + 'spiderBro_%s.log' % (start_day)

    config = get_args()
    if (config.debug_logging == True):
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logFormatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging_level)

    fileHandler = logging.FileHandler(logfilename)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
