import pytvdbapi
from pytvdbapi import api
# don't hammer thetvdb api, it times out
    
db =api.TVDB('046CE679C95B0D0C')
result = db.search('Constantine', 'en')
show = result[0]
