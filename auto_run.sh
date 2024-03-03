#!/bin/sh
cd /home/code
#gunicorn
#gunicorn main:app --workers 8 --timeout 300 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
# uvicorn
uvicorn main:app --host 0.0.0.0 --port 80
