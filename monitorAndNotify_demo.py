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
        sampleFreq = 1 # time in seconds

        ACCESS_TOKEN="o.6R644v50MdAV0UYCGevjg3dmT8ALos9z"

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
            # bad_temp = False
            # bad_humid = False
            # # JSON file 
            # f = open ('config.json', "r") 
            
            # # Reading from file 
            # config_data = json.loads(f.read())
            # comfort_minTemp = config_data['comfortable_min_temp']
            # comfort_maxTemp = config_data['comfortable_max_temp']
            # comfort_minHumid = config_data['comfortable_min_humid']
            # comfort_maxHumid = config_data['comfortable_max_humid']
            
            # # Closing file 
            # f.close()
            
            if temp is not None and humidity is not None:
                temp = round(temp, 1)
                humidity = round(humidity, 1)
                log_time = logData (temp, humidity)
            #     if temp > comfort_maxTemp or temp < comfort_minTemp: bad_temp=True
            #     if humidity > comfort_maxHumid or humidity < comfort_minHumid: bad_humid=True
            # return bad_temp, bad_humid
            return log_time

        # log sensor data on database
        def logData (temp, humidity):
            log_time = str(datetime.datetime.now().replace(microsecond=0))
            conn=sqlite3.connect(dbname)
            curs=conn.cursor()
            curs.execute("INSERT INTO SENSEHAT_data(recorded_time, temp, humidity) values(?, ?, ?)", (log_time, temp, humidity))
            conn.commit()
            conn.close()
            return log_time

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

        # notify_msg_count = 0
        # time_order = []
        # #for i in range (0,3):
        # while True:
        #     bad_temp_var, bad_humid_var = getSenseHatData()
        #     # print(bad_temp_var, bad_humid_var)
        #     # print('Bad temp: {}, bad humid: {}'.format(bad_temp_var,bad_humid_var))
        #     ip_address = os.popen('hostname -I').read()
        #     if(bad_temp_var==True or bad_humid_var==True):
        #         if(notify_msg_count==0):
        #             send_notification_via_pushbullet(ip_address, "Temperature or Humidity is out of comfortable range")
        #             sentTime = datetime.datetime.now()
        #             notify_msg_count+=1
        #             time_order.append(sentTime)
        #         elif(notify_msg_count > 0 and ((datetime.datetime.now() - time_order[len(time_order)-1]).total_seconds())>=90): #check if time difference btw last notif msg and current msg has been at least 24 hrs
        #             send_notification_via_pushbullet(ip_address, "Temperature or Humidity is out of comfortable range")
        #             sentTime = datetime.datetime.now()
        #             notify_msg_count+=1
        #             time_order.append(sentTime)
        #     time.sleep(sampleFreq) #log sensor datas after every min
        # displayData()

        bad_temp_list=[]
        bad_humid_list=[]
        counter=0
        while True:
        # for i in range (0,3):
            log_time = getSenseHatData()
            print(log_time[11:16])
            print(log_time[0:10])
            c_date=log_time[0:10]
            # if log_time[11:16]=="23:59":
            if counter==10:
                conn=sqlite3.connect(dbname)
                curs=conn.cursor()
                curs.execute("SELECT * FROM SENSEHAT_data WHERE recorded_time LIKE '%'||?||'%'", (c_date,))
                records = curs.fetchall()
                conn.close()
                for row in records:
                    bad_temp = False
                    bad_humid = False
                    if float(row[2]) > comfort_maxTemp or float(row[2]) < comfort_minTemp: bad_temp=True
                    if float(row[3]) > comfort_maxHumid or float(row[3]) < comfort_minHumid: bad_humid=True
                    if bad_temp==True:
                        bad_temp_list.append(row)
                    if bad_humid==True:
                        bad_humid_list.append(row)
                #find highest, lowest bad temp and highest, lowest bad humid of today
                bad_temp_arr=[]
                bad_humid_arr=[]
                highest_bad_temp=None
                lowest_bad_temp=None
                highest_bad_humid=None
                lowest_bad_humid=None
                if len(bad_temp_list)>0:
                    for bad_record in bad_temp_list:
                        float_temp = float(bad_record[2])
                        bad_temp_arr.append(float_temp)
                    highest_bad_temp = max(bad_temp_arr)
                    lowest_bad_temp = min(bad_temp_arr)
                    print(bad_temp_arr)
                    print(highest_bad_temp)
                    print(lowest_bad_temp)
                    if highest_bad_temp==lowest_bad_temp and highest_bad_temp!=None and lowest_bad_temp!=None:
                        if highest_bad_temp!=None:
                            if highest_bad_temp < comfort_minTemp:
                                highest_bad_temp=None
                        if highest_bad_temp!=None:
                            if highest_bad_temp > comfort_maxTemp: 
                                lowest_bad_humid=None
                    if highest_bad_temp!=None:
                        if highest_bad_temp < comfort_minTemp:
                            highest_bad_temp=None
                    if lowest_bad_temp!=None:
                        if lowest_bad_temp > comfort_maxTemp:
                            lowest_bad_temp=None
                if len(bad_humid_list)>0:
                    for bad_record in bad_humid_list:
                        float_humid = float(bad_record[3])
                        bad_humid_arr.append(float_humid)
                    highest_bad_humid = max(bad_humid_arr)
                    lowest_bad_humid = min(bad_humid_arr)
                    print(bad_humid_arr)
                    print(highest_bad_humid)
                    print(lowest_bad_humid)
                    if highest_bad_humid==lowest_bad_humid and highest_bad_humid!=None and lowest_bad_humid!=None:
                        if highest_bad_humid!=None:
                            if highest_bad_humid < comfort_minHumid:
                                highest_bad_humid=None
                        if highest_bad_humid!=None:
                            if highest_bad_humid > comfort_maxHumid:
                                lowest_bad_humid=None
                    if highest_bad_humid!=None:
                        if highest_bad_humid < comfort_minHumid:
                            highest_bad_humid=None
                    if lowest_bad_humid!=None:
                        if lowest_bad_humid > comfort_maxHumid:
                            lowest_bad_humid=None
                ip_address = os.popen('hostname -I').read()
                if len(bad_temp_list)==0 and len(bad_humid_list)==0:
                    send_notification_via_pushbullet(ip_address, "Today's temp and humid are okay")
                elif len(bad_temp_list)!=0 and len(bad_humid_list)!=0:
                    if highest_bad_temp==None and highest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp and humid are both below comfortable range. Recorded: {}C, {}%".format(lowest_bad_temp, lowest_bad_humid))
                    elif lowest_bad_temp==None and lowest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp and humid are both above comfortable range. Recorded: {}C, {}%".format(highest_bad_temp, highest_bad_humid))
                    elif highest_bad_temp==None and lowest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is below and humid is above comfortable range. Recorded: {}C, {}%".format(lowest_bad_temp, highest_bad_humid))
                    elif lowest_bad_temp==None and highest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is above and humid is below comfortable range. Recorded: {}C, {}%".format(highest_bad_temp, lowest_bad_humid))
                    elif highest_bad_temp==None and highest_bad_humid!=None and lowest_bad_humid!=None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is below and humid is out of comfortable range. Recorded: {}C, Bad Highest Humid: {}% Bad Lowest Humid: {}%".format(lowest_bad_temp, highest_bad_humid, lowest_bad_humid))
                    elif lowest_bad_temp==None and highest_bad_humid!=None and lowest_bad_humid!=None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is above and humid is out of comfortable range. Recorded: {}C, Bad Highest Humid: {}% Bad Lowest Humid: {}%".format(highest_bad_temp, highest_bad_humid, lowest_bad_humid))
                    elif highest_bad_humid==None and highest_bad_temp!=None and lowest_bad_temp!=None:
                        send_notification_via_pushbullet(ip_address, "Today's humid is below and temp is out of comfortable range. Recorded: {}%, Bad Highest Temp: {}C Bad Lowest Temp: {}C".format(lowest_bad_humid, highest_bad_temp, lowest_bad_temp))
                    elif lowest_bad_humid==None and highest_bad_temp!=None and lowest_bad_temp!=None:
                        send_notification_via_pushbullet(ip_address, "Today's humid is above and temp is out of comfortable range. Recorded: {}%, Bad Highest Temp: {}C Bad Lowest Temp: {}C".format(highest_bad_humid, highest_bad_temp, lowest_bad_temp))
                    else:
                        send_notification_via_pushbullet(ip_address, "Today's temp and humid are out of comfortable range. Recorded: Bad Highest Temp: {}C Bad Lowest Temp: {}C, Bad Highest Humid {}%, Bad Lowest Humid {}%".format(highest_bad_temp, lowest_bad_temp, highest_bad_humid, lowest_bad_humid))
                elif len(bad_temp_list)!=0 and len(bad_humid_list)==0:
                    if highest_bad_temp==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is below comfortable range and humid is fine. Recorded: {}C".format(lowest_bad_temp))
                    elif lowest_bad_temp==None:
                        send_notification_via_pushbullet(ip_address, "Today's temp is above comfortable range and humid is fine. Recorded: {}C".format(highest_bad_temp))
                    else: send_notification_via_pushbullet(ip_address, "Today's temp is out of comfortable range and humid is fine. Recorded: Bad Highest Temp: {}C Bad Lowest Temp: {}C".format(highest_bad_temp, lowest_bad_temp))
                elif len(bad_humid_list)!=0 and len(bad_temp_list)==0:
                    if highest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's humid is below comfortable range and temp is fine. Recorded: {}%".format(lowest_bad_humid))
                    elif lowest_bad_humid==None:
                        send_notification_via_pushbullet(ip_address, "Today's humid is above comfortable range and temp is fine. Recorded: {}%".format(highest_bad_humid))
                    else: send_notification_via_pushbullet(ip_address, "Today's humid is out of comfortable range and temp is fine. Recorded: Bad Highest Humid {}%, Bad Lowest Humid {}%".format(highest_bad_humid, lowest_bad_humid))
                displayData()
            counter+=1
            time.sleep(sampleFreq) #log sensor datas after every min
        
# Execute program
s1 = sensorIndicator
s1.main()