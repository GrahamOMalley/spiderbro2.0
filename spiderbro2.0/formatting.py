#! /usr/bin/env python
import unicodedata
import re

def get_torrent_name_from_magnet(torrent):
    tor = re.sub("&tr.*$", "", torrent)
    tor = re.sub("magnet.*=", "", tor)
    return tor

def format_number(no):
    """ 
    pad a zero if no < 10, else do nothing
    """
    return "0" + str(no) if(int(no)<10) else str(no)

def create_show_dir_name(series_name):
    """ 
    Uses normalization rules to change string to lowercased with _ instead of space
    and removes characters that are problematic for shell/dirnames
    """
    series_name = str.lower(series_name)
    series_name = series_name.replace("::", "")
    series_name = series_name.replace(": ", " ")
    series_name = series_name.replace(":", " ")
    series_name = series_name.replace(";", " ")
    series_name = series_name.replace("&", "and")
    series_name = series_name.replace(" ", "_") 
    series_name = series_name.replace("/", "_") 
    series_name = series_name.replace("\\", "_") 
    series_name = series_name.replace("_-_", "_") 
    series_name = "".join(ch for ch in series_name if ch not in ["!", "'", ":", "(", ")", ".", ",", "-"])
    # unicode screws up some shows, convert to latin-1 ascii
    series_name = unicode(series_name, "latin-1")
    unicodedata.normalize('NFKD', series_name).encode('ascii','ignore')
    return series_name

def get_episode_no_from_filename(file, s):
    """ 
    parse filename, return episode number
    """ 
    sNeN = re.compile(".*s01e([0-9][0-9]).*")
    gr = sNeN.findall(file)
    try:
        if(gr[0]):
            return "e"+str(gr[0])
    except:
        pass

    return "e-1"