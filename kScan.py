import os
from os.path import basename
import random
import time
import RPi.GPIO as GPIO
import credentials as login
import ldap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
GPIO.setmode(GPIO.BCM)


try:
    GPIO.cleanup()
except:
    pass


def main():
    print("Lets set up that iButton Reader")
    time.sleep(1)
    try:
        os.system('modprobe wire timeout=1 slave_ttl=5')
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-smem')
    except:
        print("You probably need to re-run this as sudo buddy...this is kinda embarrassing...\n")
        return

    print("We did it!\nGo ahead and start scanning my dude!")
    time.sleep(2)
    get_ibutton()


def saveDoc(file_name, user):
    directory = os.popen("ls /scans/").read()
    folders = directory.split()
    print(folders)
    if user not in folders:
        os.system("mkdir /scans/" + user)
        os.system("mv /scans/TMP/* /scans/" + user + "/")
	return True
    else:
        os.system("mv /scans/TMP/* /scans/" + user + "/")
        return True

    return False


def sendMail(file_name, user):
    

    attachment = "/scans/" + user + "/" + file_name
    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"
    text = MIMEText("Your scan is complete! \nIf something is wrong with this email, check out the wiki to learn another way to get your file!")
    msg = MIMEMultipart() 
    msg.attach(text)
    f = open(attachment, "rb")
    part = MIMEApplication(f.read(), Name=basename(attachment))
    part["Content-Disposition"] = 'attachment; filename="%s"' % basename(attachment)
    msg.attach(part)
    msg["Subject"] = "Here is your completed scan!"
    msg["From"] = me
    msg["To"] = you
    msg.preamble = "Here is your completed scan!"
    s = smtplib.SMTP('mail.csh.rit.edu')
    s.sendmail(me, you, msg.as_string())
    s.quit()


def goodbyeMail(user):
    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"
    msg = MIMEMultipart()
    text = MIMEText("Your scan backup has been deleted, for more info see the wiki")
    msg.attach(text)
    msg["Subject"] = "Scan Backup Deleted"
    msg["From"] = me
    msg["To"] = you
    s = smtplib.SMTP('mail.csh.rit.edu')
    s.sendmail(me, you, msg.as_string())
    s.quit()


def find_user(varID, cache={}):
    ibutton = varID.strip()
    if ibutton in cache:
        return cache[ibutton]

    try:
        #conn = ldap.initialize(login.ldap_server, bytes_mode=True)
        conn = ldap.initialize(login.ldap_server)
        conn.simple_bind_s(login.ldap_user, login.ldap_pass)
        ldap_results = conn.search_s('ou=Users,dc=csh,dc=rit,dc=edu', ldap.SCOPE_SUBTREE, "(ibutton=%s)" % ibutton,
                ['uid', 'homeDirectory'])
        print('(ibutton=%s)' % ibutton)
        return ldap_results[0][1]['uid'][0]
    except Exception as e:
        print(e)
        print("\n")
        print("were having some trouble getting your user ID, try scanning again")
        return None


def get_ibutton():
    GPIO.setup(24,GPIO.OUT)
    base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
    delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
    GPIO.output(24,True)
    startTime = time.time()

    while True:
        tick = time.time()
        if tick == startTime + 604800:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime)))
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tick)))
            startTime = time.time()
            user_dirs = os.popen("ls /scans").read()
            folders = user_dirs.split()
            for each in folders:
                if each == "TMP":
                    pass
                else:
                    os.system("rm -rf /scans/" + each)
                    goodbyeMail(each)
            os.system("mkdir /scans/TMP")

        data = open(base_dir, "r")
        ibutton = data.read()
        ibutton = ibutton.strip()
        data.close()
        if ibutton != 'not found.\n':
            GPIO.output(24,False)
            time.sleep(3)
            print(ibutton)
            try:
                user = find_user("67" + ibutton[3:] + "01")
                if user is None:
                    print("Cannot scan, ldap didn't give me a user")
                else:
                    print(user)
                    filename = takeScan(user)
                    print("scan saved as" + filename)

            except Exception as e:
                print(e)
                print("Captain, I'm afraid the ship is sinking")

            d = open(delete_dir, "w")
            d.write(ibutton)
            GPIO.output(24, True)

    d.close()
    GPIO.cleanup()


def takeScan(user):
    file_name = user + "_" + str(random.randint(0, 100)) + "_scan.jpg"
    os.system("scanimage --resolution 250 -x 215 -y 279 > /scans/TMP/" + file_name)
    
    saveDoc(file_name, user)
    sendMail(file_name, user)
    return file_name


if __name__ == "__main__":
        #main()
	#goodbyeMail(find_user("67000001ECFCC601"))
	#saveDoc(find_user("67000001ECFCC601"))
	takeScan(find_user("67000001ECFCC601"))
