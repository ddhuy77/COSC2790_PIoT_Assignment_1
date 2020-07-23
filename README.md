# COSC2790_PIoT_Assignment_1
Assignment 1 working repo of Nguyen Khac Phu - s3650959 and Dang Duc Huy - s3678636

# Usage
No cronjob was implemented

I-General Guide
To run python scripts
In terminal, cd "project_dir_name"
Then, python3 script_name.py

II-Steps to run apiRESTful.py
1. Install Python 3.8 following this guidehttps://installvirtual.com/how-to-install-python-3-8-on-raspberry-pi-raspbian/
Note: Remember to NOT Make Python 3.8 as the default version, skip this step
2. Create virtual environment for Python3.8

sudo pip3.8 install virtualenv
sudo pip3.8 install virtualenvwrapper

sudo nano ~/.bashrc

Add these lines at the bottom of bashhrc && source ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=./testing
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.8
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh
export VIRTUALENVWRAPPER_ENV_BIN_DIR=bin

Look up some commands to create, remove, deactivate a virtual env

First time initiate a virtual env
mkdir testing
cd testing
mkvirtualenv testing

Why using virtual env? To freely test project and safely install packages for new Python3.8 inside virtual env without affecting the system file of default or other versions of python setup

Install python packages required to run the script: (make sure to install these packages inside the initated virtual environment of Python3.8)
$ sudo pip3 install Flask \
    Flask-SQLAlchemy \
    Flask-RESTful \
    flask-marshmallow

Then we need to create a db file if we haven't created one
Using these commands
python3
>>from apiRESTful import db
>>db.create_all()

now inside your current directory, sensehat.db has been created

now, run the script using: python3 apiRESTful.py

test curl cmds
GET API URL (in order to get the latest record, assign id param with latest id in GET by id request method url)
curl http://localhost:5000/posts
curl http://localhost:5000/posts/1
POST API URL (to upload with current timestamp, please manually edit the recorded_time to match the current timestamp)
curl http://localhost:5000/posts -X POST -H "Content-Type: application/json" -d '{"recorded_time":"2020-01-01 00:00:00", "temp":"10", "humidity":"10"}'
PUT API URL (in order to update the latest record, assign id param with latest id in PUT request method url)
curl http://localhost:5000/posts/1 -X PATCH -H "Content-Type: application/json" -d '{"recorded_time":"2020-01-01 00:00:00", "temp":"100", "humidity":"100"}'
DELETE API URL
curl http://localhost:5000/posts/2 -X DELETE -I

To check for any data inside sensehat.db using these commands:
>>sqlite3
>>.open sensehat.db
>>select * from SENSEHAT_data;
>>(a table of data will be displayed)
>>.exit(when you're done viewing)

III-Bluetooth communication guide
First, make some installations to make bluetooth connection available between Pis following this guide: https://www.element14.com/community/docs/DOC-81266/l/setting-up-bluetooth-on-the-raspberry-pi-3
The bluetooth1.py will be run from sending devices (Pi), and bluetooth2.py from receiving devices (laptop)
Run both the scripts after 2 devices successfully paired using blueman app installed in initial setup, you should run bluetooth2.py (server code) first before running bluetooth1.py (client code). Host address is bluetooth address of Pi
Type "send" in the terminal to start sending sensor data report to device
Type "check" to detect bluetooth devices

IV-Other notes
Some optional python scripts and files: clear.py, create_db.py, launcher.sh
launcher.sh: a launcher script used to run monitorAndNotify.py in next reboot using cronjob but failed to do so (unsolved issues)
clear.py: use to reset the LED matrix display of HAT sensor
create_db.py: use to create a sqlite db file, but this is just to test for a database creation, to create db file with correct data types assigned to columns, please create it from apiRESTful following the above steps
