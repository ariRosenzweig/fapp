from flask import Flask, current_app
from celery import Celery
from datetime import timedelta
import requests, json
import bs4, lxml
from bs4 import BeautifulSoup
from functions import get_api, get_links, get_entries
from clry import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://test:test@localhost/',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
celery = make_celery(app)



@celery.task()
def fetch_url(url): 
       a =  requests.get(url).json()
       return a 
          

@celery.task()
def fetch_main(url):
    a =  requests.get(url).content.decode('utf-8')
    return a

@app.route('/api/<first_name>/<last_name>')
@app.route('/api/<first_name>/<last_name>/<state_name>')
def home(first_name, last_name):    
    urls=get_api(first_name, last_name)
    result = [fetch_url.delay(i) for i in urls]
    return_value = [i.get() for i in result]
    q = get_entries(return_value)
    links = get_links(q)    
    return{ 'number': len(links), 'links': links}

@app.route('/')
def default():
    return current_app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(debug=True)

