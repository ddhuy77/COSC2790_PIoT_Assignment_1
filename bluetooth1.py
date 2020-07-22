import bluetooth
import json
import sqlite3

class bluetoothTask:
    def runTask():
        def processRecord():
            # JSON file 
            f = open ('config_min_max.json', "r") 

            # Reading from file 
            config_data = json.loads(f.read())
            comfort_minTemp = config_data['min_temperature']
            comfort_maxTemp = config_data['max_temperature']
            comfort_minHumid = config_data['min_humidity']
            comfort_maxHumid = config_data['max_humidity']

            # Closing file 
            f.close()

            def readNewestRecord():
                dbname='sensehat.db'
                conn=sqlite3.connect(dbname)
                curs=conn.cursor()
                curs.execute("SELECT * FROM SenseHat_data WHERE ID = (SELECT MAX(ID) FROM SenseHat_data)")
                record=curs.fetchone()
                #print(record)
                conn.close()
                return record

            record=readNewestRecord()
            new_temp=float(record[2])
            new_humid=float(record[3])
            temp_status=""
            humid_status=""
            text_msg=""
            if new_temp is not None and new_temp < comfort_minTemp: #cold
                temp_status="cold"
            elif new_temp is not None and new_temp > comfort_maxTemp: #hot
                temp_status="hot"
            else: temp_status="comfortable"

            if new_humid is not None and new_humid < comfort_minHumid: #dry
                humid_status="dry"
            elif new_humid is not None and new_humid > comfort_maxHumid: #wet
                humid_status="wet"
            else: humid_status="comfortable"
            if temp_status=="comfortable" and humid_status=="comfortable":
                text_msg="Recorded: {} C, {} %. Both temp and humid are within comfortable range"
            if temp_status=="comfortable" and humid_status=="dry":
                humid_diff=str(round(comfort_minHumid-new_humid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is within and humid is {} percent below comfortable range".format(new_temp, new_humid, humid_diff)
            if temp_status=="comfortable" and humid_status=="wet":
                humid_diff=str(round(new_humid-comfort_maxHumid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is within and humid is {} percent above comfortable range".format(new_temp, new_humid, humid_diff)
            if humid_status=="comfortable" and temp_status=="cold":
                temp_diff=str(round(comfort_minTemp-new_temp,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Humid is within and temp is {} C below comfortabl range".format(new_temp, new_humid, temp_diff)
            if humid_status=="comfortable" and temp_status=="hot":
                temp_diff=str(round(new_temp-comfort_maxTemp,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Humid is within and temp is {} C above comfortabl range".format(new_temp, new_humid, temp_diff)
            if temp_status=="cold" and humid_status=="dry":
                temp_diff=str(round(comfort_minTemp-new_temp,1))
                humid_diff=str(round(comfort_minHumid-new_humid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is {} C below and humid is {} percent below comfortable range".format(new_temp, new_humid, temp_diff, humid_diff)
            if temp_status=="cold" and humid_status=="wet":
                temp_diff=str(round(comfort_minTemp-new_temp,1))
                humid_diff=str(round(new_humid-comfort_maxHumid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is {} C below and humid is {} percent above comfortable range".format(new_temp, new_humid, temp_diff, humid_diff)
            if temp_status=="hot" and humid_status=="dry":
                temp_diff=str(round(new_temp-comfort_maxTemp,1))
                humid_diff=str(round(comfort_minHumid-new_humid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is {} C above and humid is {} percent below comfortable range".format(new_temp, new_humid, temp_diff, humid_diff)
            if temp_status=="hot" and humid_status=="wet":
                temp_diff=str(round(new_temp-comfort_maxTemp,1))
                humid_diff=str(round(new_humid-comfort_maxHumid,1))
                new_temp=str(new_temp)
                new_humid=str(new_humid)
                text_msg="Recorded: {} C, {} %. Temp is {} C above and humid is {} percent above comfortable range".format(temp_diff, humid_diff)

            return text_msg
        
        #client
        serverMACAddress = '34:DE:1A:31:2B:52'
        port = 4
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((serverMACAddress, port))
        while 1:
            text = input() # Note change to the old (Python 2) raw_input
            output = processRecord()
            if text == "quit":
                break
            elif text=="check":
                print("looking for nearby devices...")
                nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True, duration = 20)
                print("found %d devices" % len(nearby_devices))
                for name, addr in nearby_devices:
                    print(" %s - %s" % (addr, name))
            elif text== "send":
                s.sendall(output.encode('utf-8'))
        sock.close()

b1=bluetoothTask
b1.runTask()