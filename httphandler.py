"""
 A module to handle HTTP connection and retrive data
 in case of error return proper error message and log
 it appropriately.
"""

from urllib2 import Request, urlopen


def connect(url):
    request = Request(url)
    request.add_header('User-Agent',"Mozilla/5.0")
    response = None
    
    try:
        response = urlopen(request).read()
    except Exception as e:
        return e

    return response
    
