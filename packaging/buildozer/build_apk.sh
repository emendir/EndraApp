
BLACK='\033[0;30m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
NC='\033[0m' # no colour

echo -e "$YELLOW
REMEMBER: If you've updated dependecies, run:"
echo -e "$MAGENTA
buildozer android clean
$NC"
docker pull ghcr.io/kivy/buildozer:latest
DOCKER_IMAGE=ghcr.io/kivy/buildozer
# DOCKER_IMAGE=local/buildozer
# the absolute path of this script's directory
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPT_DIR
# Exit if any command fails
set -e
PROJ_DIR=$(realpath $SCRIPT_DIR/../..)
WORK_DIR=$PROJ_DIR
WORK_DIR=$SCRIPT_DIR
APK_PATH=$PROJ_DIR/dist/Endra-current-debugging.apk
./prebuild.sh

if ! [ -e $WORK_DIR/.buildozer ];then
  ln -s $SCRIPT_DIR/.buildozer $WORK_DIR/.buildozer
fi

if ! [ -e ~/.buildozer ];then
  mkdir ~/.buildozer
fi


# docker run  \
#   -v $HOME/.buildozer:/home/user/.buildozer \
#   -v $WORK_DIR/buildozer.spec:/home/user/hostcwd/buildozer.spec \
#   -v $WORK_DIR/.buildozer:/home/user/hostcwd/.buildozer \
#   -v $WORK_DIR/bin:/home/user/hostcwd/bin \
#   -v $PROJ_DIR/src:/home/user/hostcwd/src \
#   $DOCKER_IMAGE android debug
# 


# SSH_ADDR=phablet@10.42.0.200
SSH_ADDR=phablet@192.168.189.125
# ssh -t $SSH_ADDR "rm -f /media/phablet/PhoneSD/waydroid/data/media/0/Download/*.apk"
# scp bin/EndraApp-0.1-arm64-v8a-debug.apk $SSH_ADDR:/media/phablet/PhoneSD/waydroid/data/media/0/Download/
# cp $WORK_DIR/bin/EndraApp-0.1-arm64-v8a-debug.apk $APK_PATH


# docker run  \
#   -v $HOME/.buildozer:/home/user/.buildozer \
#   -v $WORK_DIR/buildozer.spec:/home/user/hostcwd/buildozer.spec \
#   -v $WORK_DIR/.buildozer:/home/user/hostcwd/.buildozer \
#   -v $WORK_DIR/bin:/home/user/hostcwd/bin \
#   -v $PROJ_DIR/src:/home/user/hostcwd/src \
#   $DOCKER_IMAGE android deploy run logcat
cd $WORK_DIR
buildozer android deploy run logcat


# # Get the first connected device
# DEVICE=$(adb devices | sed -n '2p' | cut -f1)
# 
# if [ -z "$DEVICE" ]; then
#   echo "No device connected."
#   exit 1
# fi
# 
# echo "Using device: $DEVICE"
# 
# # Install the APK
# adb -s "$DEVICE" install -r "$APK_PATH"
# 
# # Extract package name from the APK (requires aapt)
# PACKAGE=$(aapt dump badging "$APK_PATH" | grep "package: name=" | sed -E "s/.*name='([^']+)'.*/\1/")
# 
# if [ -z "$PACKAGE" ]; then
#   echo "Failed to extract package name from APK."
#   exit 1
# fi
# 
# # Get the launchable activity
# ACTIVITY=$(aapt dump badging "$APK_PATH" | grep launchable-activity | sed -E "s/.*name='([^']+)'.*/\1/")
# 
# if [ -z "$ACTIVITY" ]; then
#   echo "Failed to extract launchable activity from APK."
#   exit 1
# fi
# 
# echo "Launching $PACKAGE/$ACTIVITY"
# 
# # Start the main activity
# adb -s "$DEVICE" shell am start -n "$PACKAGE/$ACTIVITY"
# 
# # Start logcat
# echo "Starting logcat (debug level)"
# adb -s "$DEVICE" logcat *:D
