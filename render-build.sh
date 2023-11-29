set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  curl -sS -O https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x google-chrome-stable_current_amd64.deb .
  rm google-chrome-stable_current_amd64.deb
else
  echo "...Using Chrome from cache"
fi

# Make sure we return to where we were
cd $HOME/project/src

# add your own build commands...
