import os
import sane
import time
import RPi.GPIO as GPIO
import credentials as login
import ldap
GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()
except:
    pass


def main():
    print("Lets set up that iButton Reader")
    time.sleep(1)

    try:
        os.system("modprobe wire timeout=1 slave_ttl=5")
        os.system("modprobe w1-gpio")
        os.system("modprobe w1-smem")
    except:
        print("You probably need to re-run this as sudo buddy...this is kinda embarrassing...\n")
        return

    print("We did it!\nGo ahead and start scanning my dude!")
    time.sleep(2)
    get_ibutton()


def find_user(varID, cache={}):
    ibutton = varID.strip()
    if ibutton in cache:
        return cache[ibutton]

    try:
        #conn = ldap.initialize(login.ldap_server, bytes_mode=True)
        conn = ldap.initialize(login.ldap_server)

        conn.simple_bind_s(login.ldap_user, login.ldap_pass)
        ldap_results = conn.search_s("ou=Users,dc=csh,dc=rit,dc=edu", ldap.SCOPE_SUBTREE, "(ibutton=%s)" % ibutton,
                ["uid", "homeDirectory"])
        print("(ibutton=%s)" % ibutton)

        return ldap_results[0][1]["uid"][0]

    except Exception as e:
        print(e)
        print("\n")
        print("were having some trouble getting your user ID, try scanning again")
        return None


def get_ibutton():
    try:
        GPIO.setup(24,GPIO.OUT)

    except:
        print("uh oh! you didn't run me as root! you gotta!")
        return 

    base_dir = "/sys/devices/w1_bus_master1/w1_master_slaves"
    delete_dir = "/sys/devices/w1_bus_master1/w1_master_remove"
    GPIO.output(24,True)

    while True:
        data = open(base_dir, "r")
        ibutton = data.read()
        data.close()
        if ibutton != "not found.\n":
            GPIO.output(24,False)
            time.sleep(3)
            print(ibutton)

            try:
                user = find_user()
                if user is None:
                    print("Cannot scan, ldap didn't give me a user")

                else:
                    print(user)
                    transferFile(user)

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
        os.system("scp " + imagepath + " " + user + "@shell.csh.rit.edu:~/.scan/")


def takeScan(user):
    ver = sane.init()
    print("SANE Version: " + ver)

    devices = sane.get_devices()
    sel_dev = sane.open(devices[0][0])

    sel_dev.start()
    print("Starting device")
    print("Scanning...")

    im = sel_dev.snap()

    im.save()
    return im


if __name__ == "__main__":
        main()
