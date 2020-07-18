import time
import datetime
import sqlite3
from sense_hat import SenseHat
import requests
import json
import os

class sensorIndicator:
    # main function
    def main():
        dbname='sensehat.db'
        sampleFreq = 60 # time in seconds

        ACCESS_TOKEN="o.6R644v50MdAV0UYCGevjg3dmT8ALos9z"

        # get data from SenseHat sensor
        def getSenseHatData():
            def tempCalibration():
                # Get CPU temperature.
                def get_cpu_temp():
                    res = os.popen("vcgencmd measure_temp").readline()
                    return float(res.replace("temp=","").replace("'C\n",""))

                # Use moving average to smooth readings.
                def get_smooth(x):
                    if not hasattr(get_smooth, "t"):
                        get_smooth.t = [x,x,x]
                    
                    get_smooth.t[2] = get_smooth.t[1]
                    get_smooth.t[1] = get_smooth.t[0]
                    get_smooth.t[0] = x
                    return (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3

                sense = SenseHat()
                t1 = sense.get_temperature_from_humidity()
                t2 = sense.get_temperature_from_pressure()
                t_cpu = get_cpu_temp()
                h = sense.get_humidity()
                p = sense.get_pressure()

                # Calculates the real temperature compesating CPU heating.
                t = (t1 + t2) / 2
                t_corr = t - ((t_cpu - t) / 1.5)
                t_corr = get_smooth(t_corr)
                return t_corr

            sense = SenseHat()
            temp = tempCalibration()
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

        notify_msg_count = 0
        time_order = []
        for i in range (0,3):
        # while True:
            bad_temp_var, bad_humid_var = getSenseHatData()
            # print(bad_temp_var, bad_humid_var)
            print('Bad temp: {}, bad humid: {}'.format(bad_temp_var,bad_humid_var))
            ip_address = os.popen('hostname -I').read()
            if(bad_temp_var==True or bad_humid_var==True):
                if(notify_msg_count==0):
                    send_notification_via_pushbullet(ip_address, "Temperature or Humidity is out of comfortable range")
                    sentTime = datetime.datetime.now()
                    notify_msg_count+=1
                    time_order.append(sentTime)
                elif(notify_msg_count > 0 and ((datetime.datetime.now() - time_order[len(time_order)-1]).total_seconds())>=90): #check if time difference btw last notif msg and current msg has been at least 24 hrs
                    send_notification_via_pushbullet(ip_address, "Temperature or Humidity is out of comfortable range")
                    sentTime = datetime.datetime.now()
                    notify_msg_count+=1
                    time_order.append(sentTime)
            time.sleep(sampleFreq) #log sensor datas after every min
        displayData()

# Execute program
s1 = sensorIndicator
s1.main()