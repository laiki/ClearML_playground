#!/bin/bash
# script used by the author on Ubuntu 20.04 

#To make sure to use the newest docker binaries let's first uninstall any docker 
#binary on the system with:

sudo systemctl stop docker.service
sleep 2
sudo apt-get remove -y docker docker-engine docker.io containerd runc docker-ce docker-ce-cli docker-compose
sleep 2
sudo systemctl start docker.service

#now the istallation begins...
#alternatively docker.com provides an easy way of istallation by:
# curl -fsSL https://get.docker.com -o get-docker.sh
# sudo sh get-docker.sh
#but let's do it menually

#To install docker from its official repository you need to add its key to the key store so the the package management will enable you to install packages from its repositoy. To be able to do this you need to run the following commands at least once on your system:

sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common 

#The following command loads the certificate over http and stores it i the key store:

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

#You should verify if the added key is the official one by checking its 'fingerprint' with: 

sudo apt-key fingerprint 0EBFCD88

#The output must be as follows:
#pub rsa4096 2017–02–22 [SCEA]
# 9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88
#uid [ unknown] Docker Release (CE deb) <docker@docker.com>
#sub rsa4096 2017–02–22 [S]
#You still need to add the docker repository to the list of repositories your system makes use of. This command adds the stable repository:

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   
#Now you can install the needed packages by calling 

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sleep 2

#Unfortunately the docker-compose installation instruction are not making use of the APT package managment. You need instead to download the binary, place it to a folder been part of your $PATH environment variable and make it executable. I guess there are some good reasons why this differs from the rest of the docker binary installation, but I don't know it. To get it call the commands:

sudo curl -L "https://github.com/docker/compose/releases/download/1.28.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER

#Check if the tools needed are available by calling them requesting their version information e.g. by `docker --version` and `docker-compose --version`. Any docker installation instruction I have seen so far are ending with a test getting and running the hello-world image, so why not doing the same, but try it without sudoing it ;)

docker run hello-world
#If you don't see the message "Hello from Docker!" you will need to double check if you followed the above instructions and repeat them.

