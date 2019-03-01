from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import api
import configparser
from timeit import default_timer as timer
import logging
from collections import Counter

def APICall(value):
    request = value
    function = getattr(api,'get'+value)
    start = timer()
    response = function(keys[value])
    end = timer()   
    latency = str(end - start)
    logging.info('|request| '+request+' |response| '+response+' |latency| '+latency)
    return response


def metrics(logPath):
    dic = {}
    with open(logPath) as fp:
        lines = fp.readlines()
    for line in lines:
        if line != '\n':
            l = line.split('|')
            if l[2] in dic.keys():
                dic[l[2]].append(l[4])
            else:
                dic[l[2]] = [l[4]]
    dic2 = {}
    for key in dic.keys():
        cn = Counter(dic[key])
        dic2[key] = []
        for k,v in cn.items():
            dic2[key].append((k,str(v)))
    return dic2

def metricsComponent():
    states = metrics(logPath)
    HTML = ''
    for title in states.keys():
        HTML += ('<h3>'+title+'</h3><ul>')
        
        for name,no in states[title]:
            HTML += ('<li>'+name+' '+no+'</li>')
        HTML += '</ul>'
    return HTML

def HTMLPage(components):
    HTML = open('Header.html').read()
    for component in components:
        HTML += component
    HTML += open('Foot.txt').read()
    return HTML

def APIComponent(name,value,selected=None):
    HTMLapi = open('ApiStart.txt').read()
    HTMLapi += 'name="' + name + '" value= "' + value + '"/> </form>'
    if selected == name:
        HTMLapi += APICall(value)
    HTMLapi += open('ApiEnd.txt').read()
    return HTMLapi


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/home'
        if self.path[1:] in ['home','metrics']:
            if self.path[1:] == 'home':
                components = [APIComponent('InternetPorvider','InternetPorvider'),APIComponent('City','City'),APIComponent('Map','Map')]
            else:
                
                components = [metricsComponent()]
            HTML = HTMLPage(components)
            self.send_response(200)
        else:
            HTML = '<h1>404 Not Found</h1>'
            self.send_response(404)
        self.end_headers()
        self.wfile.write(HTML.encode())
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(301)
        self.end_headers()
        response = BytesIO()
        response.write(body)
        selected = response.getvalue().decode().split('=')[0]
        components = [APIComponent('InternetPorvider','InternetPorvider',selected),APIComponent('City','City',selected),APIComponent('Map','Map',selected)]
        HTML = HTMLPage(components)
                
        self.end_headers()
        self.wfile.write(HTML.encode())



if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    logPath = config.get('General','log_path')
    
    keyInternetPorvider = config.get('General','key_InternetPorvider').split(',')
    keyCity = config.get('General','key_City').split(',')
    keyMap = config.get('General','key_Map').split(',')
    keys = {'InternetPorvider':keyInternetPorvider,'City':keyCity,'Map':keyMap}
    logging.basicConfig(filename=logPath,level=logging.INFO, format='%(message)s')
    httpd = HTTPServer(('localhost',8080), Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        raise























