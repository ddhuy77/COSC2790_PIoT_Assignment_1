#sudo crontab -e
#Add this line at the bottom and save
#@reboot sh /home/pi/COSC2790_PIoT_Assignment_1/launcher.sh >/home/pi/logs/cronlog 2>&1
#script will be run on next reboot
cd /
cd home/pi/PIoT_A1/COSC2790_PIoT_Assignment_1
sudo python3 monitorAndNotify.py &
cd /