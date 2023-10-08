#!/bin/bash
set -x

sudo apt update
sudo apt upgrade -y

# Set up Python
sudo apt-get -y install python3-pip

python3 --version

# Install Theresa
mkdir -p /home/ubuntu/theresa
cd /home/ubuntu/theresa
mv ../theresa.tar.gz .
tar -xf theresa.tar.gz
rm theresa.tar.gz

pip3 install --upgrade pip
pip3 install tensorflow
python3 -m pip install .
cd /home/ubuntu/

# Install Nginx and load SSL config
sudo apt install -y nginx
sudo mv /home/ubuntu/nginx.conf /etc/nginx/sites-enabled/default
