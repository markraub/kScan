import os
import random
import time
import RPi.GPIO as GPIO
import credentials as login
import ldap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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


def saveDoc(user):

    directory = os.popen("ls /scans").read()
    folders = directory.split()

    if user not in folders:

        os.system("mkdir /scans/" + user)
        saveDoc(user)

    else:

        os.system("mv /scans/TMP /scans/" + user)

        return True

    return False


def sendMail(user):

    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"

    text = MIMEText("Your scan is complete! \nIf something is wrong with this email, check out the wiki to learn another way to get your file!")

    fp = open("/scans/" + user, 'rb')
    msg = MIMEImage(fp.read())
    fp.close()

    msg["Subject"] = "Here is your completed scan!"
    msg["From"] = me
    msg["To"] = you


    s = smtplib.SMTP('mail.csh.rit.edu')
    p = smtplib.SMTP_SSL_PORT('465')
    s.sendmail(me, you, text)
    s.quit()

def goodbyeMail(user):

    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"

    msg = MIMEText("Scans Deleted")

    text = MIMEText("Your scan folder has been deleted, for more info see the wiki")


    msg["Subject"] = "Scan Folder Deleted"
    msg["From"] = me
    msg["To"] = you

    s = smtplib.SMTP('mail.csh.rit.edu')
    p = smtplib.SMTP_SSL_PORT('465')
    s.sendmail(me, you, text)
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
                                takeScan(user)
                                sendMail(user)
                                saveDoc(user)

                        except Exception as e:

                            print(e)
                            print("Captain, I'm afraid the ship is sinking")

                        d = open(delete_dir, "w")
                        d.write(ibutton)
                        GPIO.output(24, True)

        d.close()
        GPIO.cleanup()

def transferFile(user):

        if user is not None:

            takeScan(user)
            imagepath = "/scans/" + user + ".jpeg"
            os.system('scp ' + imagepath + " " + user + "@shell.csh.rit.edu:~/.scan/")


def takeScan(user):

    os.system("scanimage --resolution 400 -x 215 -y 279 > /scans/TMP/" + user + "_" + str(random.randint(0, 100)) + "_scan.jpg")


if __name__ == "__main__":

        main()
