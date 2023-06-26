#!/bin/bash
set -x

# Install Python 3.10
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.10 -y
sudo apt install python3-pip -y
sudo apt install python3.10-venv -y
alias python=python3.10
alias python3=python3.10

git clone https://$GH_PAT_READ@github.com/QubitPi/theresa.git
cd /home/ubuntu/theresa
sudo pip3 install flask flasgger
