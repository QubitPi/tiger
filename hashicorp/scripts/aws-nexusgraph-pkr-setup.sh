#!/bin/bash
set -x
set -e

sudo mv /home/ubuntu/server.crt /etc/ssl/certs/server.crt
sudo mv /home/ubuntu/server.key /etc/ssl/private/server.key
