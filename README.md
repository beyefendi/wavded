# Web App Vulnerability Discovery &amp; Exploit Development

## Perspective

- In this course, we focus on logical vulnerabilities that many web scanners fail to detect.
- We aim to discover a series of vulnerabilities that can only-together lead to system compromise.
- We are learning how to exploit "chained vulnerabilities" to grant shell.
- We are interested in "authentication bypass" and then "remote code execution".
- We develop fully automated "single-click" exploitation scripts.
- In principle, we perform blackbox analysis for identification of available functionalities.
- Then, we apply whitebox analysis for vulnerability discovery.

## Learning objectives

- Environmental settings for whitebox analysis
  - PHP, MySQL, VSCode, xdebug debugger
  - Java, PostgreSQL, JD-GUI decompiler, process explorer
- Identification of potential vulnerabilities to help authentication bypass
  - Analyze publicly accessible webpages
    - Identification of user input fields
    - Identification of application user roles
    - Boolean-based blind SQLi
    - Time-based blind SQLi
- Identification of potential vulnerabilities for authentication bypass
  - Analyze login process
    - Lack of session token validation
    - Insecure password forgot mechanism
- Identification of potential vulnerabilities for code execution
  - Analyze functionalities of the application
    - File upload
    - Command injection
    - JS injection
    - SST injection
    - Deserialization

## CS571 Schedule

<details>
  <summary>Week 0x00 | Setting up environment</summary>

- **VM**
  - Kali, Ubuntu
- **Exploit development tools**
  - VSCode
    - Python3, NodeJS, Java, PHP, C#
  - Reversing
    - JD-GUI Java decompiler
    - dnSpy .NET debugger
  - jar_builder.sh
  - python3 -m http.server 80
  - nc -nlvp 9090
- **Traffic analysis tools**
  - openvpn without typing creds
  - /etc/hosts
  - SSH (SOCKS + forwarding)
  - BurpSuite
    - Add to scope + Show only inscope items
    - Request handling
    - Invisible proxying
  - FoxyProxy
    - Blacklists
    - Use enabled proxies
- **Methodology**
  - Enable application logging
  - Enable database query logging
  - Static source code analysis tools
  - Browse webpages
  - Identify unauthenticated code sections
  - Identify user input sanitization mechanism
  - Identify SQL statement building mechanism
  - Identify dangerous function usage i.e. eval()
  - Analyze authentication functions i.e. password reset, remember me, etc.
  - Analyze promising functions i.e. file upload, backup etc. 
  - Debug (+ print statements)

</details>

<details>

  <summary>Week 0x01 | Blind boolean SQLi & Bypass session token & File upload</summary>

- **Credentials**
  - Weak input sanitization (i.e. overriding $addslashes() for vulnerability!)
  - Handle payload restrictions for SQLi (i.e. equivalent characters)
  - Dump hashed password
- **Authentication bypass**
  - Lack of session token validation
  - Login by pass-the-hash
- **Remote code execution**
  - Improper usage of die() function (i.e. prevents extracted files to be deleted)
  - Escape from default upload directory (i.e. Directory traversal)
  - Discover web root directory (i.e. error messages, display_errors = on)
  - Find out a writable directory under web root
  - Improper xml validation
  - Bypass file extension filter
  - Upload shell
  - Automate full process
  - Gain unauthorized privileged shell access

</details>

<details>

  <summary>Week 0x02 | Blind boolean SQLi & Type juggling & File upload</summary>

- **Credentials**
  - Same as Week 1
  - Dump unique member_id and account creation_date
- **Authentication bypass**
  - Allowing user e-mail update without authentication
  - Loose comparisons results in the execution of implicit data type conversions
  - Type conversion for "scientific exponential number notation"
  - Magic hash values
  - Comparing only first n char of a hash value
  - Brute force
- **Remote code execution**
  - Same as Week 1

</details>

<details>

  <summary>Week 0x03 | Blind time-based SQLi & File upload</summary>

- **Credentials**
  - No authentication control (isAuthenticated()) for wiewItem.php
  - Logic error: Lack of die() function usage (Although 302 redirection, code flow continues)
  - Escaping quote is not bullet proof
  - SQL parameters aren't surrounded with quote
  - Time-based blind sqli
  - Dump username
  - Dump token of password change
- **Authentication bypass**
  - Token is written to database (not a session token)
  - Token is not generated based on time
  - Change password via token
  - Login by changed password
- **Remote code execution**
  - Upload folder is under web root
  - No mimes control for updateItem.php
  - Bypass file extension filter (.phar)
  - Upload shell
  - Automate full process
  - Gain unauthorized privileged shell access

</details>

<details>

  <summary>Week 0x04 | Insecure random & XXE</summary>

- **Authentication bypass**
  - java.util.Random() function is vulnerable
  - Identifying EPOCH range (timestamp & Date header)
  - Timezone issues
  - Generate list of possible tokens
  - Start spraying attempt from the beginning or end or ?
  - Send request until finding the valid token (throttling or lockout ?)
  - Cannot login with the credentials set, but wait
- **Remote code execution**
  - Finding API documentations (sample requests/responses)
  - Bypass API Basic Authentication
  - Bypass API Basic Authentication
  - XML parser configuration is vulnerable
  - Bypassing XML parser errors
  - XML character escaping
  - CDATA + wrapper
  - External entitiy
  - XML entity for reading file content
  - Read web app server credentials
  - Read web db server credentials
  - Connect HSQLDB
  - Create a funtion to query system information
  - Create a SP for file upload
  - Minimize jsp cmd shell to fit in 1KB restriction
  - Upload jsp cmd shell
  - Download jsp reverse shell via cmd shell
  - Popping reverse shell
</details>
