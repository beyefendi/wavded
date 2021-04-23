# Author: Emre SUREN
# Usage: ./jarbuiler GenerateToken
BUILD_DIR="build-jar/"
META_DIR=$BUILD_DIR"META-INF/"
MANIFEST=$META_DIR"MANIFEST.MF"
JAVA_FILE=$1

rm -rf $BUILD_DIR
mkdir $BUILD_DIR
mkdir $META_DIR
echo "Main-Class: $JAVA_FILE" > $MANIFEST 

javac -d $BUILD_DIR $JAVA_FILE.java
echo "[+] Compiled"

cd $BUILD_DIR
jar cvmf ../$MANIFEST $JAVA_FILE.jar $JAVA_FILE.class
echo "[+] Jar generated"

cd ..
rm $BUILD_DIR$1.class
rm -rf $META_DIR
ls -hl $BUILD_DIR

echo "[+] Testing: Executing jar"
email="admin@target.local"
salt="2ef6f49d-5ede"
token="O109R1pLUD"
mode="encrypt"
java -jar $BUILD_DIR$JAVA_FILE.jar $email $salt $token $mode