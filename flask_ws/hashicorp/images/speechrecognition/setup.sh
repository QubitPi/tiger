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

# Setup Flask
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r speechrecognition/requirements.txt

cd /home/ubuntu/
