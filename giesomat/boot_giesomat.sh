#!/bin/sh
#Script to boot the giesomat app

docker run -d --rm --hostname giesomat-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3.10.0-rc.3-management-alpine #Run the rabbit MQ container
#sudo -u pi -s
#cd 
cd /home/pi/giesomat/giesomat
gunicorn giesomat.wsgi --bind 0.0.0.0:8080 --daemon #Start the django application via gunicorn
python /home/pi/giesomat/giesomat/giesomat_app/rpi/boot_rpi.py #Setup the GPIO

celery -A giesomat_app worker --loglevel=INFO --detach #Start a celery worker for the giesomat_app
celery -A giesomat_app beat --loglevel=INFO --detach #Start celery beat for the giesomat_app
