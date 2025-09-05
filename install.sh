#!/usr/bin/bash
# does the following:
# - DeckyCloudRsync Decky Plugin
if [ "$EUID" -eq 0 ]
  then echo "Please do not run as root"
  exit
fi


echo "Removing previous install if it exists"

cd $HOME

sudo rm -rf $HOME/homebrew/plugins/DeckyCloudRsync

echo "Installing DeckyCloudRsync for savedata cloud sync"
# download + install simple decky tdp
curl -L $(curl -s https://api.github.com/repos/Emiliopg91/DeckyCloudRsync/releases/latest | grep "browser_download_url" | cut -d '"' -f 4) -o $HOME/DeckyCloudRsync.tar.gz
sudo tar -xzf DeckyCloudRsync.tar.gz -C $HOME/homebrew/plugins

# Install complete, remove build dir
rm  $HOME/DeckyCloudRsync.tar.gz
sudo systemctl restart plugin_loader.service

echo "Installation complete"
