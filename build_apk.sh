
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
"
docker pull ghcr.io/kivy/buildozer:latest
DOCKER_IMAGE=ghcr.io/kivy/buildozer
DOCKER_IMAGE=local/buildozer
# the absolute path of this script's directory
script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $script_dir
# Exit if any command fails
set -e

./prebuild.sh

if ! [ -e ~/.buildozer ];then
  mkdir ~/.buildozer
fi

# ./build_buildozer_docker.sh
docker run -v $HOME/.buildozer:/home/user/.buildozer -v $(pwd):/home/user/hostcwd $DOCKER_IMAGE android debug


# SSH_ADDR=phablet@10.42.0.200
SSH_ADDR=phablet@192.168.189.125
# ssh -t $SSH_ADDR "rm -f /media/phablet/PhoneSD/waydroid/data/media/0/Download/*.apk"
# scp bin/nfsApk-0.1-arm64-v8a-debug.apk $SSH_ADDR:/media/phablet/PhoneSD/waydroid/data/media/0/Download/


buildozer android deploy run logcat