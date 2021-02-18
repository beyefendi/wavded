# Web App Vulnerability Discovery &amp; Exploit Development

## Perspective

- In this course, we are learning how to exploit "chained vulnerabilities" to grant shell.
- Basically, we focus on "authentication bypass" and then "remote code execution".
- We develop fully automated "single-click exploitation" scripts.
- In principle, we perform blackbox analysis for identification of available functionalities .
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
