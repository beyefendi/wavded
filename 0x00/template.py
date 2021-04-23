import sys
import requests
import hashlib

protocol= "http://"
rhost   = ""
proxies = {} #{ 'http': 'http://localhost:8080' } #{'http': 'socks4://localhost:8181'} #

def login(username, password):
    
    path            = "/ATutor/login.php"
    target          = "%s%s%s" % (protocol, rhost, path)

    d = {
        "username": username,
        "password" : password,
        "submit": "Login"
    }
    
    sess = requests.Session()
    r = sess.post(target, data=d)
    
    res = r.text
    
    if "Welcome" in res:
        print("[+] Authentication successful")
    else:
        print("[-] Authentication failure!")
    
    return sess

def auth_bypass():
    pass

def rce(username, password):
    login(username, password)

def main():
    if len(sys.argv) != 3:
        print("[!] usage: %s <rhost> <lhost> <lport>" % sys.argv[0])
        print('[!] eg: python %s target.remote 192.168.2.26 9090' % sys.argv[0])
        sys.exit(-1)

    global rhost
    rhost = sys.argv[1]
    
    username = "emre"
    password = "Zz987654."
    
    auth_bypass()
    
    rce(username, password)

    
if __name__ == "__main__":
    main()