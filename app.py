# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 19:09:53 2016

@author: RaoUmer
"""

from flask import Flask, render_template, request
import os
import requests
import formasaurus as ffd
import urllib
from urllib2 import Request, urlopen, URLError


app = Flask(__name__)

cur_dir = os.path.dirname(__file__)

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val


def formdetect(url):
    fd = []
    html = requests.get(url).text
    fdetection = ffd.extract_forms(html)
    for i in range(len(fdetection)):
        for j in range(len(fdetection[i])):
            fd.append(fdetection[i][j])
    #fd = [{'fields': {'s': 'search query'}, 'form': u'search'}]
    return fd 

# Flask App
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')



@app.route('/search', methods=['GET','POST'])
def search():
    return render_template('search.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/results', methods=['GET','POST'])
def results():
    # url_list = ["http://autos.columnpk.net/", "http://driver.pk/"]
    #url = "http://autos.columnpk.net/"
    #url = "http://www.google.com/"
    #url = "https://www.olx.com.pk/vehicles/"
    #url = "http://autos.columnpk.net/"
    url = "http://driver.pk/"
    #url = "http://www.pkmotors.com/"    
    #url = "http://cardealer.com.pk/"   
    #url = "http://sastigari.com/search/cars/"
    
    if request.method == 'POST': 
        fd = formdetect(url)
        for item in fd:
            if "fields" in item:
                if DictQuery(item).get("fields/s") == 'search query' or DictQuery(item).get("fields/q") == 'search query' or DictQuery(item).get("fields/full_search") == 'search query' or DictQuery(item).get("fields/txtKeyword") == 'search query' or DictQuery(item).get("fields/cmbPMax") == 'search category / refinement' or DictQuery(item).get("fields/cmbPMin") == 'search category / refinement':
                    if DictQuery(item).get("fields/s"):
                        values = {'s' : str(request.form['query'])}
                    elif DictQuery(item).get("fields/txtKeyword"):  
                        values = {'txtKeyword' : str(request.form['query'])}
                    else:
                        values = {'q' : str(request.form['query'])}
        
#                if DictQuery(item).get("fields/cmbPMax"):
#                    values = {'cmbPMax' : str(request.form['max'])}
#                
#                if DictQuery(item).get("fields/cmbPMin"):
#                    values = {'cmbPMin' : str(request.form['min'])}
                
                    data = urllib.urlencode(values)
                    req = Request(url, data)
                    
                    try:
                        response = urlopen(req)
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print 'We failed to reach a server.'
                            print 'Reason: ', e.reason
                        elif hasattr(e, 'code'):
                            print 'The server couldn\'t fulfill the request.'
                            print 'Error code: ', e.code
                        else:
                            content = response.read()
                            with open("templates/query_results.html", "w") as f:
                                f.write(content)                
            else:
                continue
                
    return render_template('results.html')
    
#    else:
#        fd = formdetect(url)
#        for item in fd:
#            if "fields" in item:
#                if DictQuery(item).get("fields/mk") == 'search category / refinement': 
#                    if DictQuery(item).get("fields/mk"):  
#                        #values = {'condition' : 'used', 'md':'','mk' : '2578', 'price[t]' : '2000000', 'price[f]' : '1000000' }
#                        data = {}
#                        #data['condition'] = 'used'
#                        #data['md'] = ''
#                        data['mk'] = str(request.form['query'])
#                        data['price[t]'] = str(request.form['max'])
#                        data['price[f]'] = str(request.form['min'])
#                
#                    url_values = urllib.urlencode(data)
#                    full_url = url + '?' + url_values
#                    response = urlopen(full_url)                
#                    content = response.read()
#                    with open("templates/query_results.html", "w") as f:
#                            f.write(content)                
#            else:
#                continue      
#        return render_template('results.html')

@app.route('/queryresults', methods=['GET','POST'])
def queryresults():
    return render_template('query_results.html')
        
if __name__ == '__main__':
    app.run(debug=True)
