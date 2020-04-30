Clone and cd into directory
Run flask run in one shell.
Run below commands in 3 Saperstein shells. All are done in the root directory of the project

celery -A fapp.celery worker -l info --concurrency=100 --pool=eventlet  -Q queue1

celery -A fapp.celery worker -l info --concurrency=100 --pool=eventlet  -Q queue2

celery -A fapp.celery worker -l info -Q queue3
