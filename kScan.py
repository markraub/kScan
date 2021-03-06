import os
import random
import time
import RPi.GPIO as GPIO
#import get_ibutton
import mail_sender
import beeps
import threading
from roxasauth import roxasauth
import json

api_key = "8206636300fe27b345b5101c474a2880c8ea8d52"

GPIO.setmode(GPIO.BCM)

try:
   GPIO.cleanup()

except:

    pass

def delScans():

    user_dirs = os.popen("ls /scans").read()
    folders = user_dirs.split()

    for each in folders:

        if each == "TMP":

            pass

        else:

            os.system("rm -rf /scans/" + each)
            mail_sender.goodbyeMail(each)



def main():


    try:
        
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)
    except:
        print("[" + time.strftime('%y-%m-%d %H:%M:%S', time.localtime()) + "] GPIO pins not set" )
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    GPIO.output(24, True)
    start_time = time.time()

    while True:

        tick = time.time()
        if tick == start_time + 604800:

            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tick)))

            start_time = time.time()
            delScans()

        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()

        if not 'not' in ibutton:
            GPIO.output(24, False)
            #beeps.beep(400, 500)
            #time.sleep(1)
            print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] iButton found!" + ibutton)

            try:
                #user = get_ibutton.find_user(ibutton[3:] + "01")
                rox_obj = roxasauth(api_key)
                ibutton_format = ibutton[3:] + "01"
                rox_dic = rox_obj.ibutton(ibutton_format, ["uid"])
                if rox_dic is None:
                    print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] Cannot scan, ldap didn't give me a user")
                else:
                    
                    if rox_dic["can_access"]:

                        user = rox_dic["returned_attrs"]["uid"]
                        print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] iButton read! you must be " + user)
                        file_name = takeScan(user)

                        mail_sender.sendMail(file_name, user)

                        print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] scan saved as " + file_name)
                    else:

                        print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] user does not have access ")

            except Exception as e:
                print(e)
                print("[" + time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.localtime()) + "] Captain, I'm afraid the ship is sinking")

            d = open(delete_dir, "w")
            d.write(ibutton)
            GPIO.output(24, True)

    d.close()
    GPIO.cleanup()


def saveDoc(file_name, user):

    directory = os.popen("ls /scans/").read()
    folders = directory.split()

    if user not in folders:

        os.system("mkdir /scans/" + user)
        os.system("mv /scans/TMP/" + file_name + " /scans/" + user + "/")

    else:

        os.system("mv /scans/TMP/" + file_name + " /scans/" + user + "/")

        print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] File saved in /scans/" + user)


def takeScan(user):

    file_name = user + "_" + str(int(time.time())) + "_scan.jpg"
    
    os.system("cp /home/markraub/Github/kScan/yes.html /var/www/html/index.html")

    os.system("scanimage --resolution 300 -x 215 -y 279 > /scans/TMP/" + file_name)

    print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] scan complete")

    #beeps.march()

    os.system("mogrify -resize 90% /scans/TMP/" + file_name)

    saveDoc(file_name, user)

    os.system("cp /home/markraub/Github/kScan/no.html /var/www/html/index.html")

    return file_name

def glow():

    GPIO.cleanup()

    p = GPIO.PWM(24, 100)

    for i in range(0, 100):

        p.ChangeDutyCycle(i)

    for i in range(0, 100):

        p.ChangeDutyCycle(100-i)


if __name__ == "__main__":

    main()
    #delScans()

