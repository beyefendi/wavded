# Web App Vulnerability Discovery &amp; Exploit Development

## Perspective

- In this course, we are learning how to exploit "chained vulnerabilities" to grant shell.
- Basically, we focus on "authentication bypass" and then "remote code execution".
- We develop fully automated "single-click exploitation" scripts.
- In principle, we perform blackbox analysis for identification of available functionalities .
- Then, we apply whitebox analysis for vulnerability discovery.

## Learning objectives

- Environmental settings for whitebox analysis (PHP, MySQL, VSCode debugger)
- Identification of potential vulnerabilities to help authentication bypass
  - Analyze publicly accessible webpages
    - Identification of user input fields
    - Identification of application user roles
    - Blind boolean SQLi
- Identification of potential vulnerabilities for authentication bypass
  - Analyze login process
    - Lack of session token validation
- Identification of potential vulnerabilities for code execution
  - Analyze functionalities of the application
    - File upload
    - Command injection
    - JS injection
    - SST injection
    - Deserialization

## CS571 Schedule

<details>

  <summary>Week 0x01 | Blind Boolean SQLi & Bypass session token & File upload</summary>

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
