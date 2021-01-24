#!/bin/bash

# adapt max virtual memory settings needed by elastic search
echo "vm.max_map_count=262144" > /tmp/99-clearml.conf
sudo mv /tmp/99-clearml.conf /etc/sysctl.d/99-clearml.conf
sudo sysctl -w vm.max_map_count=262144

# restart docker service
sudo service docker restart

# create folder structure used by clearml-server
sudo rm -R /opt/clearml/
sudo mkdir -p /opt/clearml/data/elastic_7
sudo mkdir -p /opt/clearml/data/mongo/db
sudo mkdir -p /opt/clearml/data/mongo/configdb
sudo mkdir -p /opt/clearml/data/redis
sudo mkdir -p /opt/clearml/logs
sudo mkdir -p /opt/clearml/config
sudo mkdir -p /opt/clearml/data/fileserver
sudo chown -R 1000:1000 /opt/clearml

# get the YML file and place it into the clearml server folder
sudo curl https://raw.githubusercontent.com/allegroai/clearml-server/master/docker/docker-compose.yml -o /opt/clearml/docker-compose.yml
sudo chown $USER /opt/clearml/docker-compose.yml

