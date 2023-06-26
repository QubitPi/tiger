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

# The next install is to fix the following error during "sudo python3 -m venv .venv" in Terraform:
#
# The virtual environment was not created successfully because ensurepip is not
# available.  On Debian/Ubuntu systems, you need to install the python3-venv
# package using the following command.
#
#     apt install python3.8-venv
# You may need to use sudo with that command.  After installing the python3-venv
# package, recreate your virtual environment.
#
# Failing command: ['/home/ubuntu/theresa/.venv/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']
sudo apt install python3.8-venv -y

git clone https://$GH_PAT_READ@github.com/QubitPi/theresa.git
cd /home/ubuntu/theresa
sudo pip3 install flask flasgger
