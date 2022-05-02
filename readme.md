#Giesomat


```
This is a leraning project where we built a plant watering system based driven by a raspberry pi.
```

## SSH to the RPI

```
ssh pi@raspberrypi.local
exit ssh
```


##Installation

```
sudo apt-get update && sudo apt-get upgrage
```

###Install docker
```
curl -SSL https://get.docker.com | sh
```
Grant access for your ssh user
```
sudo usermod -aG docker pi
```

### Run rabbitmq on docker

It is important to find a rabbitmq docker image that fits your system architecture.
My system architecture is linux/arm/v6 and the latest image that supports this architecture is 3.10.0-rc.3-management-alpine.
```
docker pull rabbitmq:3.10.0-rc.3-management-alpine
```
Run the docker image:
```
docker run -d --rm --hostname giesomat-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3.10.0-rc.3-management-alpine
Check the status of your container
```
docker ps -a
docker logs [container id]
```


### Setup git on your rpi and pull the repo

git configuration and clone repo
```
git config --global user.name "your user name"
git config --global user.email email.adress@gmail.com
git clone https://github.com/janis50000/giesomat
```

Install dependencies
navigate to the giesomat repo before installing dependencies.
```
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

Configure the Django app

```
python3 -m django makemigrations --settings=giesomat.settings
python3 -m django migrate --settings=giesomat.settings
```

Create a superuser for your app
```
python3 manage.py createsuperuser
```

Make sure that the RPI gets automatically setup on boot:

To execute the boot scripts script on boot up, do the following:
cd .. to the root of the rpi and navigate tho the following file:
```
sudo nano /etc/rc.local
```

Edit this file with the following lines and save:
```
docker run -d --rm --hostname giesomat-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3.10.0-rc.3-management-alpine &
python -c 'from /home/pi/giesomat/giesomat/giesomat_app/rpi/boot_rpi.py import boot_rpi; boot_rpi()' &
python -c 'from /home/pi/giesomat/giesomat/giesomat_app/backend_logic/initialize.py import initialize_hardware; initialize_hardware()' &
```

Obsolete
#python /home/pi/giesomat/init_pins_on_boot.py &
#python /home/pi/giesomat/relay_test.py &
$ python -c 'from foo import hello; print hello()'


Test if everything works as designed
```
cd giesomat/giesomat
python manage.py test giesomat_app
```

Now you are ready to rumble
```
cd giesomat/giesomat
python manage.py runserver
```


##Main Cababilities:
UI to display current values in a gauge (Gießcounter per day or last sensor value)
UI to display values over time (Sensor Wert über den Tag, Flüssigkeit über die Zeit)
Admin views to maintain plants, the watering hardware and schedulers

###3 Cron Jobs. 
- 1 Job to read the sensors
- 1 Job to water plants based on humidity level
- 1 Job to water plants based on a fixed schedule


###Plant States:
- HAPPY
- THIRSTY
- WATERED

HAPPY => THIRSTY: Sensor below Threshold
THIRSTY => THIRSTY: Sensor (still) below Threshold
THIRSTY => WATERED: Plant has been watered
WATERED => HAPPY: Sensor above Threshold
WATERED => THIRSTY: SENSOR (still) below Threshold
