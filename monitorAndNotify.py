import time
import sqlite3
from sense_hat import SenseHat
import requests
import json
import os
dbname='sensehat.db'
sampleFreq = 1 # time in seconds

ACCESS_TOKEN="o.6R644v50MdAV0UYCGevjg3dmT8ALos9z"

# get data from SenseHat sensor
def getSenseHatData():	
    sense = SenseHat()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    bad_temp = False
    bad_humid = False
    # JSON file 
    f = open ('config.json', "r") 
    
    # Reading from file 
    config_data = json.loads(f.read())
    comfort_minTemp = config_data['comfortable_min_temp']
    comfort_maxTemp = config_data['comfortable_max_temp']
    comfort_minHumid = config_data['comfortable_min_humid']
    comfort_maxHumid = config_data['comfortable_max_humid']
    
    # Closing file 
    f.close()
	
    if temp is not None and humidity is not None:
        temp = round(temp, 1)
        humidity = round(humidity, 1)
        logData (temp, humidity)
        if temp > comfort_maxTemp or temp < comfort_minTemp: bad_temp=True
        if humidity > comfort_maxHumid or humidity < comfort_minHumid: bad_humid=True
    return bad_temp, bad_humid

# log sensor data on database
def logData (temp, humidity):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data(recorded_time, temp, humidity) values(datetime('now'), ?, ?)", (temp, humidity))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    """
    data_send = {"type": "note", "title": title, "body": body}
 
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 
                         'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

# main function
def main():
    notify_msg_count = 0
    for i in range (0,3):
        bad_temp_var, bad_humid_var = getSenseHatData()
        print(bad_temp_var, bad_humid_var)
        time.sleep(sampleFreq)
    displayData()
    ip_address = os.popen('hostname -I').read()
    send_notification_via_pushbullet(ip_address, "From Raspberry Pi")

# Execute program 
main()