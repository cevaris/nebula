import urllib2

def http_get(url=False):
    
    if not url:
        return False
       
    response = urllib2.urlopen(url)
    data = response.read()
    return data

def unicode_to_acsii(data):
    if isinstance(data, dict):
        return {unicode_to_acsii(key): unicode_to_acsii(value) for key, value in data.iteritems()}
    elif isinstance(data, list):
        return [unicode_to_acsii(element) for element in data]
    elif isinstance(data, unicode):
        return data.encode('utf-8','replace')
    else:
        return data
    
def http_get_json(url):
    
    response = False
    data = False

    if url:
        resposne = http_get(url)
    else:
        return False
    
    if resposne:
        data = unicode_to_acsii(resposne)
    else:
        return False
    
    return data
        
        



class TwoStepOAuth():
    
    def _request_auth(self):
        raise NotImplementedError()
    def _request_access(self):
        raise NotImplementedError()

class Oauth():
    
    def __init__(self):
        self._request_auth()
    
    def _request_auth(self):
        raise NotImplementedError()
    
    
        
        
    
def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

        
        
        
        
        
