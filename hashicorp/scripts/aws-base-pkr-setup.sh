#!/bin/bash
set -x

sudo apt update
sudo apt upgrade -y

# Set up Python
sudo apt-get -y install python3-pip
pip3 install --upgrade pip
sudo apt -y install python3.10-venv

python3 --version

# Install Theresa
mkdir -p /home/ubuntu/theresa
cd /home/ubuntu/theresa
mv ../theresa.tar.gz .
tar -xf theresa.tar.gz
rm theresa.tar.gz
cd /home/ubuntu/

# Install Nginx and load SSL config
sudo apt install -y nginx
sudo mv /home/ubuntu/nginx.conf /etc/nginx/sites-enabled/default
