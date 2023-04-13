#!/bin/bash

# initial updates
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install unzip -y

# anaconda setup
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
# User will need to page down or hit f or space to get past the MORE prompt
echo -ne "ENTER \n yes \n \n yes \n" | bash Anaconda3-2023.03-Linux-x86_64.sh
rm Anaconda3-2023.03-Linux-x86_64.sh

# terraform setup
wget https://releases.hashicorp.com/terraform/1.4.2/terraform_1.4.2_linux_amd64.zip
sudo unzip terraform_1.4.2_linux_amd64.zip -d /usr/bin
rm terraform_1.4.2_linux_amd64.zip