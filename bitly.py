import simplejson, urllib, string

API_KEY = ''
API_LOGIN = ''
API_BASE = 'http://api.bit.ly/v3'

class BitlyAPIError(Exception):
  pass

def shorten(longUrl, **kwargs):
  """
  Given a longUrl, returns a shorter one using the optionally provided keyword if possible.
  If the keyword is not available a standard hashed URL will be returned.
  
  Parameters:
    longUrl (required): URL to shorten
                        ie: shorten('http://cnn.com')
    domain (optional):  sets the preferred domain (j.mp or bit.ly <default is bit.ly>)
                        ie: shorten('http://cnn.com', domain='j.mp')
    x_login (optional): sets the end users login and API key when making requests
    x_apiKey (optional):on behalf of another bit.ly user.
                        ie: shorten('http://cnn.com', x_login='bitly', x_apiKey='ABC')
                            will add this shortening to the history of user 'bitly'
  """
  kwargs.update({
    'format': 'json',
    'login': API_LOGIN,
    'apiKey': API_KEY,
    'longUrl': longUrl,
  })
  url = API_BASE + '/shorten?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if 'ERROR' in result:
    raise BitlyAPIError, result['errorMessage']
  return result['data']['url']

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

def validate(x_login, x_apiKey, **kwargs):
  """
  Given an end users's login and API Key, determine that the pair is valid.
  
  Parameters:
    x_login (optional):   sets the end user's login
    x_apiKey (optional):  sets the end user's API key
  """
  kwargs.update({
    'format': 'json',
    'login': API_LOGIN,
    'apiKey':API_KEY,
    'x_login': x_login,
    'x_apiKey': x_apiKey,
  })
  if not (kwargs.has_key('x_login') and kwargs.has_key('x_apiKey')):
    raise BitlyAPIError, "You must provide both the end user's login and API key."
  
  url = API_BASE + '/validate?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if result['data']['valid'] == 1:
    return True
  else:
    return False

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

def stats(**kwargs):
  """
  Given a bit.ly url or hash, return traffic and referrer data.
  
  Parameters:
    shortUrl: a single URL to get stats for
              ie: expand(shortUrl='http://bit.ly/QJhM')
    hash: one or more URL hashes to get stats for
              ie: expand(hash='QJhM,3el7')
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
  
  url = API_BASE + '/stats?' + urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  if kwargs.has_key('hash'):
    return result['results']
  else:
    return result['results'][string.split(kwargs['shortUrl'], '/')[-1]]

def errors(**kwargs):
  """ Get a list of API error codes. """
  kwargs.update({
      'version': API_VERSION,
      'format': 'json',
      'login': API_LOGIN,
      'apiKey': API_KEY,
      })
  url = API_BASE + '/errors?' +urllib.urlencode(kwargs)
  result = simplejson.load(urllib.urlopen(url))
  return result['results']
