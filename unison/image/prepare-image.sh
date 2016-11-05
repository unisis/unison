#!/bin/bash

# This script is used to create a new node image based on Ubuntu.
# It's automatically copied and executed by UniSon on a new temporary
# droplet when a distro have an empty custom_image_id (create new image)
# The idea is prepare in advance all the requirements which are common
# for all nodes (not related to a specific installation)

function get_config()
{
    CONFIG_FILE=$1
    CONFIG_NAME=$2
    CONFIG_VALUE=`cat /etc/unisis/$CONFIG_FILE.conf | grep $CONFIG_NAME | cut -d "=" -f 2- | tr -d "\n"`
    echo $CONFIG_VALUE
}

# Start of script
set -e
set -x

# We don't need indicate that we are preparing the image because during
# this execution the port of SSH is changed from 22 to 2222 and UniSon
# try to connect via 22, so this script is not re-executed.

# Receive variables to be used
NGINX_PORT=$(get_config general PORT_NGINX)
SMTP_HOST=$(get_config general SMTP_HOST_NAME)
SMTP_PORT=$(get_config general SMTP_PORT_NUMBER)
SMTP_USER=$(get_config general SMTP_USER_NAME)
SMTP_PWD=$(get_config general SMTP_USER_PWD)
SMTP_SENDER=$(get_config general SMTP_SENDER_ADDRESS)
SMTP_ALERTS=$(get_config general SMTP_ALERTS_RECIPIENT)
DOCKERHUB_EMAIL=$(get_config general DOCKERHUB_EMAIL)
DOCKERHUB_AUTH=$(get_config general DOCKERHUB_AUTH)

# Current directory of script
CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configure terminal
echo "TERM=xterm" >> /etc/environment
source /etc/environment

# Since DigitalOcean use SSD disks, they don't recommend the use of SWAP
# (see https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04)
# However, since Odoo and Postgresql are memory hungry, we will create the swap,
# but we will configure swapiness=10 to only use it when it's really necessary.
if [ ! -e /var/swap.img ]; then
   # Create 4 GB swap file
   cd /var
   touch swap.img
   chmod 600 swap.img
   dd if=/dev/zero of=/var/swap.img bs=1024k count=4000
   mkswap /var/swap.img
   swapon /var/swap.img
   free
   echo "/var/swap.img    none    swap    sw    0    0" >> /etc/fstab
fi

# Update packages
apt-get update

# Install Docker
echo deb http://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list
apt-key adv --keyserver pgp.mit.edu --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
apt-get update
apt-get -y install lxc-docker

# Prepare auth file for Docker
rm -rf $HOME/.docker
mkdir -p $HOME/.docker
CONFIG_FILE=$HOME/.docker/config.json
cp /etc/unisis/config.json $CONFIG_FILE
sed -i $CONFIG_FILE -e s,{DOCKERHUB_EMAIL},"$DOCKERHUB_EMAIL",g
sed -i $CONFIG_FILE -e s,{DOCKERHUB_AUTH},"$DOCKERHUB_AUTH",g

# This file is used to disable the 'ping protocol' and configure swapiness
cp /etc/unisis/sysctl.conf /etc/sysctl.conf
sysctl -p

# This file is used to configure SSH service on port 2222 without allow password-based auth
cp /etc/unisis/sshd_config /etc/ssh/sshd_config
service ssh restart

# This file is used to launch the containers at boot time
cp /etc/unisis/rc.local /etc/rc.local
chmod +x /etc/rc.local

# Install Monit
apt-get -y install monit
wget https://mmonit.com/monit/dist/binary/5.15/monit-5.15-linux-x64.tar.gz -O /tmp/monit.tar.gz
tar xvfz /tmp/monit.tar.gz  -C /tmp
mv /tmp/monit-5.15/bin/monit /usr/bin/monit
CONFIG_FILE=/etc/monit/monitrc
cp /etc/unisis/monitrc $CONFIG_FILE

# Configure Monit
sed -i $CONFIG_FILE -e s,{SMTP_HOST},"$SMTP_HOST",g
sed -i $CONFIG_FILE -e s,{SMTP_PORT},"$SMTP_PORT",g
sed -i $CONFIG_FILE -e s,{SMTP_USER},"$SMTP_USER",g
sed -i $CONFIG_FILE -e s,{SMTP_PWD},"$SMTP_PWD",g
sed -i $CONFIG_FILE -e s,{SMTP_SENDER},"$SMTP_SENDER",g
sed -i $CONFIG_FILE -e s,{SMTP_ALERTS},"$SMTP_ALERTS",g
rm -rf /etc/monitrc
ln -s $CONFIG_FILE /etc/monitrc
service monit restart

# Define host mounts for volumes (we use source so it's executed in the same shell
# and variables defined on prepare-dirs.sh are also available on this script)
# NOTE: On real servers a volume will be mounted on /mnt/vol; this script creates the same dirs on the image disk just to launch the containers for first time.
source /root/prepare-dirs.sh

# Stop and delete any possible containers from a previous/failed
# execution (useful when we test and debug this script)
set +e
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null
set -e

###################################
# Create Aeroo Docs container

docker run --detach \
    --name=aeroo \
    --hostname aeroo \
    --env TERM=xterm \
unisis/aeroo

###################################
# Create BarMan container

docker run --detach \
    --name barman \
    --hostname barman \
    --dns=127.0.0.1 \
    --volume $BARMAN_DATA:/var/lib/barman \
    --volume $BARMAN_LOGS:/var/log/barman \
    --env TERM=xterm \
    unisis/barman /bin/bash /root/start.sh

###################################
# Create Postgresql container

docker run --detach \
    --name pgsql \
    --hostname pgsql \
    --dns=127.0.0.1 \
    --volume $PGSQL_DATA:/var/lib/postgresql \
    --volume $PGSQL_LOGS:/var/log/postgresql \
    --env TERM=xterm \
    unisis/pgsql /bin/bash /root/start.sh

###################################
# Create Odoo container (we open
# port 22 for remote debugging)

docker run --detach \
    --name odoo \
    --hostname {NODE_NAME}.{MAIN_DOMAIN} \
    --dns=127.0.0.1 \
    --volume $ODOO_ADDONS:/mnt/addons \
    --volume $ODOO_CONF:/etc/odoo \
    --volume $ODOO_DATA:/var/lib/odoo \
    --volume $ODOO_LOGS:/var/log/odoo \
    --volume $ODOO_SOURCE:/opt/odoo \
    --publish 0.0.0.0:22:22 \
    --env TERM=xterm \
    unisis/odoo /bin/bash /root/start.sh

###################################
# Create NginX container (port 80 
# opened to force redirect to 443)

docker run --detach \
    --name nginx \
    --hostname nginx \
    --dns=127.0.0.1 \
    --publish 0.0.0.0:80:80 \
    --publish 0.0.0.0:443:$NGINX_PORT \
    --env TERM=xterm \
    --volume $NGINX_CERT:/etc/nginx/certs \
    --volume $NGINX_LOGS:/var/log/nginx \
    unisis/nginx /bin/bash /root/start.sh

###################################
# Create PhpPgAdmin container

docker run --detach \
    --name phppgadmin \
    --link pgsql:pgsql \
    --publish 0.0.0.0:8000:80 \
    rkowen/postgresql-admin:9.3.4

###################################
# Create cAdvisor container

docker run --detach \
    --name cadvisor \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:rw \
    --volume=/sys:/sys:ro \
    --volume=/var/lib/docker/:/var/lib/docker:ro \
    --publish=8080:8080 \
    google/cadvisor:latest

###################################
# Stop containers (to make snapshot)
docker stop cadvisor
docker stop phppgadmin
docker stop nginx
docker stop odoo
docker stop pgsql
docker stop barman
docker stop aeroo

exit 0
