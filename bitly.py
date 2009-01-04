import simplejson, urllib

API_KEY = ''
API_LOGIN = ''
API_VERSION = '2.0.1'
API_BASE = 'http://api.bit.ly'

class BitlyAPIError(Exception):
  pass

def shorten(longUrl, **kwargs):
  kwargs.update({
    'version': API_VERSION,
    'format': 'json',
    'login': API_LOGIN,
    'apiKey': API_KEY,
    'longUrl': longUrl,
  })
  url = API_BASE + '/shorten?' + urllib.urlencode(kwargs)
  print url
  result = simplejson.load(urllib.urlopen(url))
  if 'ERROR' in result:
    raise BitlyAPIError, result['Error']
  if result['results'][longUrl]['shortKeywordUrl'] == "":
    return result['results'][longUrl]['shortUrl']
  else:
    return result['results'][longUrl]['shortKeywordUrl']

