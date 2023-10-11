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

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker ${USER}
su - ${USER}

# Install HanLP MLflow model
cd /home/ubuntu/theresa/mlflow_models/HanLPner
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 HanLPner.py
cd /home/ubuntu/theresa/mlflow_models/models/HanLPner
mlflow models build-docker --name "entity-extraction"
cd /home/ubuntu/