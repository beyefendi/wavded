# Accessing application

- Ubuntu VM (for exploit development)
  - **code.local**
  - eth0 - **192.168.2.4**
  - VsCode + Python
  - Firefox + FoxyProxy
  - Burp
  - SSH (SOCKS proxy + Port forward)
- Kali VM
  - **kali.local**
  - eth0 - **192.168.2.3**
  - eth1 - **10.10.2.3**
- Remote server (over VPN)
  - **target.remote**
  - eth0 - **10.10.2.5**
  - Application under test **target.remote:8000**

## 1) Local Burp (8080)

- Burp > Proxy > Options > Proxy listeners - **127.0.0.1:8080**
- Listen on **127.0.0.1 8080**
- Cannot access application under test

## 2) Remote Burp (8080)

- Allows access everywhere that **192.168.2.3** can access, including **10.10.2.3:8000**
  - Average performance + Easy settings
  - If **target.remote** needs to load files from external domains, it can
  - **NOTE:** Applicable for every tool
- `echo "10.10.2.5 target.remote" >> /etc/hosts`
- Burp > Proxy > Options > Proxy listeners - **192.168.2.3:8080**
  - **NOTE:** not listening on **127.0.0.1**
- Firefox
  - FoxyProxy **192.168.2.3:8080**
  - Browse **target.remote:8000** or **10.10.2.5:8000**
- Python
  - `proxies = {192.168.2.3:8080}`
  - Request **target.remote:8000** or **10.10.2.5:8000**

## 3) SOCKS proxy (8181) + Burp (8080)

- Allows access everywhere that **192.168.2.3** can access, including **10.10.2.3:8000**
  - Average performance
  - If **target.remote** needs to load files from external domains, it can
  - **NOTE:** SOCKS proxy method is only applicable for tools which can use proxy
- `echo "10.10.2.5 target.remote" >> /etc/hosts`
  - Is it really required ???
- `ssh -fN -D 8181 researcher@192.168.2.3 -i ~/Downloads/id_rsa-kali`
  - Listens on port **127.0.0.1:8181**
  - SSH to **192.168.2.3:22**
  - Forwards **8181** to **192.168.2.3** proxy
- Burp
  - Proxy > Options > Proxy listeners - **127.0.0.1:8080**
  - User options > Connections > SOCKS proxy - **127.0.0.1:8181**
- Firefox
  - Direct access
    - FoxyProxy **SOCKS4 > 127.0.0.1:8181**
    - Browse **target.remote:8000** or **10.10.2.5:8000**
  - Over Burp
    - FoxyProxy **127.0.0.1:8080**
    - Same as direct access
- Python
  - Direct access
    - `proxies = {socks4://localhost:8181}`
    - Request **target.remote:8000** or **10.10.2.5:8000**
  - Over Burp
    - `proxies = {127.0.0.1:8080}`
    - Same as direct access

## 4) Local port forwarding (8000) + Burp (8080)

- Allows access only to **10.10.2.3:8000** via **127.0.0.1:8000** or **target.remote:8000**
  - Good performance
  - If **target.remote** needs to load files from external domains, it cannot
  - **NOTE:** Applicable for every tool
- `echo "127.0.0.1 target.remote" >> /etc/hosts`
- `ssh -fN -L 8000:10.10.2.3:8000 researcher@192.168.2.3 -i ~/Downloads/id_rsa-kali`
  - Listens on port **127.0.0.1:8000**
  - SSH to **192.168.2.3:22**
  - Forwards **8000** to **10.10.2.3:8000** over SSH tunnel
- Burp > Proxy > Options > Proxy listeners - **127.0.0.1:8080**
- Firefox
  - Direct access
    - Browse **127.0.0.1:8000** or **target.remote:8000** to access **10.10.2.5:8000**
  - Over burp
    - FoxyProxy **127.0.0.1:8080**
    - Same as direct access
- Python
  - Direct access
    - `proxies = {}`
    - Request **127.0.0.1:8000** or **target.remote:8000**
  - Over Burp
    - `proxies = {127.0.0.1:8080}`
    - Same as direct access

## 5) Burp request handling

- When to use request handling

### Misconfiguration of the domain address

- target.remote - **10.10.2.5:8000**
  - web server is started on port **8000**
  - web app deployed in, but
- IP or domain address is misconfigured in application settings i.e ***http://localhost***
  - meaning that, all URLs are expected to be i.e. ***localhost:8000/login.php***
  - most common problem in wordpress installations, to check with
  - `select * from wp_options where option_value like 'http://'`
- Burp > Proxy > Options > Proxy listeners > Request handling - **10.10.2.5 8000**
  - Forwards all requests to **10.10.2.5 8000**
  - Browse or request to **http://localhost/login.php**
- (Optional) Burp > Project > Hostname Resolution
  - **target.remote** - **10.10.2.5**
  - add this information, when you are not able to modify `/etc/hosts` entries

### Lack of TLS support

- example.local - **10.10.2.5:8000**
  - configured to serve on TLS
  - meaning that, accessible only over **https://10.10.2.5:8000**
- The tool *i.e. a crawler* has a proxy support but lacking of TLS support
- Burp
  - Proxy > Options > Proxy listeners > Request handling - **10.10.2.5 8080**
  - Proxy > Options > Proxy listeners > Request handling - **Force use of TLS** enable
  - Forwards all requests to **10.10.2.5 8080** with TLS support, meaning that **https://10.10.2.5:8080**
  - Browse or request to **http://10.10.2.5:8080/login.php**

### Lack of Proxy support

- The tool *i.e. a crawler* doesn't have a proxy support
- **Invisible proxying** allows non-proxy-aware clients (a tool that doesn't support HTTP proxies) to connect directly to a proxy listener

- `echo "127.0.0.1 target.remote" >> /etc/hosts`
  - need to  modify DNS resolution to redirect inbound requests
  - tool resolves the domain name to localhost, and send requests to the proxy listeners on that interface

- Burp > Proxy > Options > Proxy listeners > Request handling - **Support invisible proxying** enable
  - to receive the redirected requests
