import credentials as login
import csh_ldap
import os


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
