web: gunicorn --bind 0.0.0.0:$PORT app:fapp

worker1:celery -A fapp.celery worker -l info --concurrency=100 --pool=eventlet  -Q queue1

