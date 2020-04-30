web: gunicorn --bind 0.0.0.0:$PORT app:app

worker1:celery -A fapp.celery worker -l info --concurrency=100 --pool=eventlet  -Q queue1
worker2: celery -A fapp.celery worker -l info --concurrency=100 --pool=eventlet  -Q queue2
worker3: celery -A fapp.celery worker -l info -Q queue3
