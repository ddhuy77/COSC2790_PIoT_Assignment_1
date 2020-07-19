import sqlite3
import json
import csv
from sense_hat import SenseHat

sense = SenseHat()
class exportCSV:
    def getDailyTemp():
        # JSON file 
        f = open ('config.json', "r") 

        # Reading from file 
        config_data = json.loads(f.read())
        comfort_minTemp = config_data['comfortable_min_temp']
        comfort_maxTemp = config_data['comfortable_max_temp']

        # Closing file 
        f.close()

        dateArr = []
        dbname='sensehat.db'
        conn=sqlite3.connect(dbname)
        curs=conn.cursor()
        #curs.execute("INSERT INTO SENSEHAT_data(recorded_time, temp, humidity) values(?, ?, ?)", ("2016-01-01 10:20:05",0, 0))
        for row in curs.execute("SELECT recorded_time FROM SenseHat_data"):
            dateArr.append(row[0])
            print(dateArr)

        #Remove duplicate dates
        res=[]
        dateArr_2=[]
        for x in dateArr:
            y=x[0:10]
            print("y: "+str(y))
            if y not in res:
                res.append(y)
                dateArr_2.append(x)
        # print(res)
        print(dateArr_2)

        with open('report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Status"])
            for d in dateArr_2:
                for row in curs.execute("SELECT * FROM SenseHat_data WHERE recorded_time=?", (d,)):
                    print(row)
                    new_temp = float(row[2])
                    if new_temp is not None and (comfort_minTemp < new_temp < comfort_maxTemp): #comfortable
                        writer.writerow([row[1], "OK"])
                    elif new_temp is not None and new_temp < comfort_minTemp: #cold
                        writer.writerow([row[1], "BAD: %d °C below the comfort temperature" % (comfort_minTemp-new_temp)])
                    elif new_temp is not None and new_temp > comfort_maxTemp: #hot
                        writer.writerow([row[1], "BAD: %d °C above the comfort temperature" % (new_temp-comfort_maxTemp)])

#Execute program
e1=exportCSV
e1.getDailyTemp()