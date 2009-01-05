import simplejson, urllib

API_KEY = ''
API_LOGIN = ''
API_VERSION = '2.0.1'
API_BASE = 'http://api.bit.ly'

class BitlyAPIError(Exception):
  pass

def shorten(longUrl, **kwargs):
	"""
	Given a longUrl, returns a shorter one using the optionally provided keyword if possible.
	If the keyword is not available a standard hashed URL will be returned.
	
	Parameters:
		longUrl (required): URL to shorten
<<<<<<< HEAD:bitly.py
		                    ie: http://cnn.com
		keyword (optional): preferred keyword
		                    ie: cnn
=======
		                    ie: shorten('http://cnn.com')
		keyword (optional): preferred keyword
		                    ie: shorten('http://cnn.com', keyword='cnn')
>>>>>>> 94612f5... skeleton of expand:bitly.py
	"""
  kwargs.update({
    'version': API_VERSION,
    'format': 'json',
    'login': API_LOGIN,
    'apiKey': API_KEY,
    'longUrl': longUrl,
  })
  url = API_BASE + '/shorten?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if 'ERROR' in result:
    raise BitlyAPIError, result['errorMessage']
  if result['results'][longUrl]['shortKeywordUrl'] == "":
    return result['results'][longUrl]['shortUrl']
  else:
    return result['results'][longUrl]['shortKeywordUrl']

def expand(**kwargs):
	"""
	Given a bit.ly url or hash(es), return the long source url(s).
	
	Parameters:
	  shortUrl: a single URL to expand
	            ie: expand('http://bit.ly/QJhM')
	  hash: one or more URL hashes to expand
	            ie: expand('QJhM,3el7')
	"""
	kwargs.update({
		'version': API_VERSION,
		'format': 'json',
		'login': API_LOGIN,
		'apiKey':API_KEY,
	})