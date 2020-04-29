from celery import Celery
from functions import process_json, requests


def make_celery(app):
    
    #celery = Celery(
        #app.import_name,
        #backend=app.config['CELERY_RESULT_BACKEND'],
        #broker=app.config['CELERY_BROKER_URL']
    #)
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = Celery()
@celery.task()
def fetch_url(url): 
       a =  requests.get(url).json()
       return a 

@celery.task()
def fetch_main(url):
    b =  requests.get(url).text
    return b

@celery.task()
def get_json(i):
    return process_json(i)