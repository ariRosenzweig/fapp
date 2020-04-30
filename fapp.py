from flask import Flask, current_app, Response
from functions import *
from clry import *


def create_app():
    app = Flask(__name__)
    # CELERY_BROKER_URL
    app.config['CELERY_BROKER_URL'] = 'amqp://test:test@localhost/'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
    app.config['CELERY_CREATE_MISSING_QUEUES'] = True
    app.config['CELERY_IMPORTS'] = 'tasks'
    make_celery(app)
    return app


app = create_app()
     

@app.route('/api/<first_name>/<last_name>')
@app.route('/api/<first_name>/<last_name>/<state_name>')
def home(first_name, last_name):    
    urls=get_api(first_name, last_name)
    result = [fetch_url.apply_async(args=[i], queue='queue1') for i in urls]
    return_value = [i.get() for i in result]
    q = get_entries(return_value)
    links = get_links(q)
    mains= [fetch_main.apply_async(args=[n], queue='queue2') for n in links]
    html_doc = [n.get() for n in mains]
    soups=[soup_it(i) for i in html_doc]
    data= [extract_json(i) for i in soups]
    inter=[get_json.apply_async(args=[i], queue='queue3') for i in data] 
    d=[i.get() for i in inter]  
    js=json.dumps(d, indent=1)
    resp = Response(js, status=200, mimetype='application/json')
    return resp  

@app.route('/api/graphs/<key>')
def make_graph(key):
    data = get_key(key)
    resp = Response(data, status=200, mimetype='application/json')
    return resp

@app.route('/')
def default():
    return current_app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(debug=True)

