import sqlite3
import json
from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
class tempIndicator02:
    def tempIndicator():
        sense = SenseHat()
        g = (0, 255, 0)
        b = (0, 0, 255)
        r = (255, 0, 0)

        dbname='sensehat.db'

        # JSON file 
        f = open ('config.json', "r") 

        # Reading from file 
        config_data = json.loads(f.read())
        comfort_minTemp = config_data['comfortable_min_temp']
        comfort_maxTemp = config_data['comfortable_max_temp']

        # Closing file 
        f.close()

        def readNewestTemp():
            conn=sqlite3.connect(dbname)
            curs=conn.cursor()
            curs.execute("SELECT * FROM SenseHat_data WHERE ID = (SELECT MAX(ID) FROM SenseHat_data)")
            record=curs.fetchone()
            print(record)
            latest_temp=record[2]
            print(latest_temp)
            conn.close()
            return latest_temp
        new_temp=float(readNewestTemp())
        if new_temp is not None and (comfort_minTemp < new_temp < comfort_maxTemp): #comfortable
            # sense.clear(g)
            sense.show_message(str(new_temp)+"C",text_colour=[0, 255, 0])
        elif new_temp is not None and new_temp < comfort_minTemp: #cold
            # sense.clear(b)
            sense.show_message(str(new_temp)+"C",text_colour=[0, 0, 255])
        elif new_temp is not None and new_temp > comfort_maxTemp: #hot
            # sense.clear(r)
            sense.show_message(str(new_temp)+"C",text_colour=[255, 0, 0])

t1=tempIndicator02
while True:
    t1.tempIndicator()
    sleep(5)
    #sleep(59)
    sense.clear()
    sleep(1)