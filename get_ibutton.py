import credentials as login
import csh_ldap
import os


def init():

    print("Lets set up that iButton Reader")

    try:
        os.system('modprobe wire timeout=1 slave_ttl=5')
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-smem')

    except:

        print("You probably need to re-run this as sudo buddy")
        exit()

    print("We did it!\nGo ahead and start scanning my dude!")


def find_user(varID):

    ibutton = varID.strip()
    ibutton = "*" + ibutton
    try:

        instance = csh_ldap.CSHLDAP(login.ldap_user, login.ldap_pass)

        user = instance.get_member_ibutton(ibutton)

        return user.uid

    except Exception as e:

        print(e)
        print("\n")
        print("were having some trouble getting your user ID, try scanning again")
        return None

if __name__ == "__main__":

    print(find_user("000001ECFCC601"))