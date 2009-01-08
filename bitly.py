import simplejson, urllib, string

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
                        ie: shorten('http://cnn.com')
    keyword (optional): preferred keyword
                        ie: shorten('http://cnn.com', keyword='cnn')
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
              ie: expand(shortUrl='http://bit.ly/QJhM')
    hash: one or more URL hashes to expand
              ie: expand(hash='QJhM,3el7')
  """
  kwargs.update({
    'version': API_VERSION,
    'format': 'json',
    'login': API_LOGIN,
    'apiKey':API_KEY,
  })
  
  if not (kwargs.has_key('shortUrl') or kwargs.has_key('hash')):
    raise BitlyAPIError, "You must provide either a shortUrl or hash."
  if (kwargs.has_key('shortUrl') and kwargs.has_key('hash')):
    raise BitlyAPIError, "You must provide either a shortUrl or hash, not both."
  
  url = API_BASE + '/expand?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if 'ERROR' in result:
    raise BitlyAPIError, result['errorMessage']
  if kwargs.has_key('hash'):
    return result['results']
  else:
    return result['results'][string.split(kwargs['shortUrl'], '/')[-1]]['longUrl']

def info(**kwargs):
  """
  Given a bit.ly url or hash, return information about that page.
  
  Parameters:
    shortUrl: a single URL to get info for
              ie: expand(shortUrl='http://bit.ly/QJhM')
    hash: one or more URL hashes to get info for
              ie: expand(hash='QJhM,3el7')
    keys (optional): one or more keys to limit attributes about each document.
              ie: expand(hash='QJhM', keys='htmlTitle,users')
  """
  kwargs.update({
      'version': API_VERSION,
      'format': 'json',
      'login': API_LOGIN,
      'apiKey': API_KEY,
      })
  
  if not (kwargs.has_key('shortUrl') or kwargs.has_key('hash')):
    raise BitlyAPIError, "You must provide either a shortUrl or hash."
  if (kwargs.has_key('shortUrl') and kwargs.has_key('hash')):
    raise BitlyAPIError, "You must provide either a shortUrl or hash, not both."
  
  url = API_BASE + '/info?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if kwargs.has_key('hash'):
    return result['results']
  else:
    return result['results'][string.split(kwargs['shortUrl'], '/')[-1]]
