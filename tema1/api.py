import urllib.request
import json
import ipinfo


def getName(string):
    return string.split(' ')[1]

def getInternetPorvider(accessToken):
    
    handler = ipinfo.getHandler(accessToken[0])
    details = handler.getDetails()
    return getName(details.org)

def getIP(accessToken):
    
    handler = ipinfo.getHandler(accessToken)
    details = handler.getDetails()
    return details.ip

def getCity(accessKey):
    
    url ='http://api.ipstack.com/'
    ip = getIP(accessKey[0])
    url = url + ip + '?access_key=' + accessKey[1]
    json_obj = urllib.request.urlopen(url)
    data = json.load(json_obj)
    return getName(data['region_name'])

def getMap(accessKey):
    
    wegit = '<iframe width="600" height="450" frameborder="0" style="border:0" '    
    query = 'src="https://www.google.com/maps/embed/v1/place?q='
    query = query + '+' +getCity(accessKey[:2])
    query = query + '+' + getInternetPorvider(accessKey[:1])
    key = '&key=' + accessKey[2]
    wegit = wegit + query + key + '" allowfullscreen></iframe>'
    return wegit


def rezultat(par1,par2):
    if par1 > par2:
        return "bravo ovidiu"
    else:
        return "hei prietene"
