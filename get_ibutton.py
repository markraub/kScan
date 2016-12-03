import credentials as login
import ldap
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

    try:
        #conn = ldap.initialize(login.ldap_server, bytes_mode=True)
        conn = ldap.initialize(login.ldap_server)
        conn.simple_bind_s(login.ldap_user, login.ldap_pass)
        ldap_results = conn.search_s('ou=Users,dc=csh,dc=rit,dc=edu', ldap.SCOPE_SUBTREE, "(ibutton=*%s)" % ibutton,
                ['uid', 'homeDirectory'])
        return ldap_results[0][1]['uid'][0]

    except Exception as e:

        print(e)
        print("\n")
        print("were having some trouble getting your user ID, try scanning again")
        return None