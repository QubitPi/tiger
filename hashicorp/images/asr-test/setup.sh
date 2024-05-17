#!/bin/bash
set -x
set -e

sudo apt update
sudo apt upgrade -y

# Set up Python
sudo apt-get -y install python3-pip
pip3 install --upgrade pip
sudo apt -y install python3.10-venv
PATH=$PATH:/home/ubuntu/.local/bin

python3 --version

# Install Nginx and load SSL config
sudo apt install -y nginx
sudo mv /home/ubuntu/fullchain.pem /etc/ssl/certs/server.crt
sudo mv /home/ubuntu/privkey.pem /etc/ssl/private/server.key
sudo mv /home/ubuntu/nginx.conf /etc/nginx/sites-enabled/default
# ASR inferencing takes lots of time. We will need to prevent Nginx time-out with the following
# https://stackoverflow.com/a/54605177
sudo mv /home/ubuntu/custom.conf /etc/nginx/conf.d/custom.conf

# Setup Flask
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r asr/requirements.txt

cd /home/ubuntu/
