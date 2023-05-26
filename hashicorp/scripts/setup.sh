#!/bin/bash
set -x

sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 -y
sudo apt install python3-pip -y

git clone https://$GH_PAT_READ@github.com/QubitPi/theresa.git
cd /home/ubuntu/theresa
sudo pip3 install flask flasgger spacy
sudo python3 -m spacy download en_core_web_sm
