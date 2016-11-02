
from urllib2 import urlopen, HTTPError
from random import choice
import json
import os
import stat



def read_ibutton(varID, cache={}):
    '''
    Use Nick Depinet's LDAP service to convert iButtons to usernames

    Caches values when possible (iButtons don't really change)
    '''
    if varID in cache:
        return cache[varID]
    try:
        data = urlopen('http://www.csh.rit.edu:56124/?ibutton=' + varID)
        uidData = json.load(data)
    except HTTPError as error:
        # Need to check its an 404, 503, 500, 403 etc.
        print(error.read())
    except ValueError as error:
        # Got malformed JSON somehow
        print(error)
    if 'error' not in uidData:
        cache[varID] = uidData['uid'], uidData['homeDir']
        return cache[varID]
    else:
        print('iButton: {} not found!'.format(varID.rstrip()))
    return "", ""

