#!/bin/bash

# Once a node/droplet is started with their attached volume,
# this script is executed by UniSon to initialize the volume
# if it's new (first mount) and to start their containers
# configuring their IPs etc. The prepare-image.sh script
# has already installed the requirements which are common
# to all the nodes (all installations). This scripts works
# on what is specific to this node/installation

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

# Load values of variables from general.conf
S3_ACCESS_KEY=$(get_config general S3_ACCESS_KEY)
S3_SECRET_KEY=$(get_config general S3_SECRET_KEY)
S3_BUCKET_BACKUPS=$(get_config general S3_BUCKET_BACKUPS)
PGSQL_PORT=$(get_config general PGSQL_PORT)
ODOO_PORT=$(get_config general PGSQL_PORT)
NGINX_PORT=$(get_config general NGINX_PORT)

# Load values of variables from install.conf
S3_BACKUPS_DIR=$(get_config install S3_BACKUPS_DIR)
IS_TEST=$(get_config install IS_TEST)
DB_NAME=$(get_config install DB_NAME)
DB_USER=$(get_config install DB_USER)
DB_PWD=$(get_config install DB_PWD)
ODOO_LANGUAGE=$(get_config install ODOO_LANGUAGE)
ADMIN_PWD=$(get_config install ADMIN_PWD)
DNS_NAME=$(get_config install DNS_NAME)
REQUEST_TIMEOUT=$(get_config install REQUEST_TIMEOUT)

# Define data directories for containers
/bin/bash /root/prepare-dirs.sh

# Start containers providing some config files

###############################################
# Start Aeroo Docs container
docker start aeroo

# Wait for initialization
sleep 15

# Get private IP
AEROO_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' aeroo | tr -d '\n')

###############################################
# Start BarMan container  (initialization later)
docker start barman

# Create file with config values used by Barman
rm -rf $BARMAN_CONF/unison.conf
touch $BARMAN_CONF/unison.conf
echo "S3_ACCESS_KEY=$S3_ACCESS_KEY" >> $BARMAN_CONF/unison.conf
echo "S3_SECRET_KEY=$S3_SECRET_KEY" >> $BARMAN_CONF/unison.conf
echo "S3_BUCKET_BACKUPS=$S3_BUCKET_BACKUPS" >> $BARMAN_CONF/unison.conf
echo "S3_BACKUPS_DIR=$S3_BACKUPS_DIR" >> $BARMAN_CONF/unison.conf

# Get private IP
BARMAN_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' barman | tr -d '\n')

###############################################
# Start Postgresql container (initialization later)
docker start pgsql

# Create file with config values used by Postgresql
rm -rf $PGSQL_CONF/unison.conf
touch $PGSQL_CONF/unison.conf
echo "IS_TEST=$IS_TEST" >> $PGSQL_CONF/unison.conf
echo "PGSQL_PORT=$PGSQL_PORT" >> $PGSQL_CONF/unison.conf
echo "DB_NAME=$DB_NAME" >> $PGSQL_CONF/unison.conf
echo "DB_USER=$DB_USER" >> $PGSQL_CONF/unison.conf
echo "DB_PWD=$DB_PWD" >> $PGSQL_CONF/unison.conf

# Get private IP
PGSQL_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' pgsql | tr -d '\n')

################################################
# Initialize Postgresql and Barman containers
# providing the mutual IP addresses of their services

docker exec barman set-host pgsql.local $PGSQL_HOST
docker exec pgsql set-host barman.local $BARMAN_HOST

docker exec barman /bin/bash /root/init.sh &
sleep 15

docker exec pgsql /bin/bash /root/init.sh &
sleep 30

###############################################
# Start Odoo

# REPOS_INFORMATION variable will be expanded as several lines (one per addons repository)
# writting their url on a config file so the start script clone those repos
ODOO_REPOS=$ODOO_CONF/repos.conf
cp /etc/unisis/repos.conf $ODOO_REPOS

# MODULES_INFORMATION variable will be expanded as several lines (one per module to install at startup)
# so -if this is the first execution of Odoo- it install these modules using the --init parameter
ODOO_MODULES=$ODOO_CONF/modules.conf
cp /etc/unisis/modules.conf $ODOO_MODULES

# Create file with config values used by Odoo
rm -rf $ODOO_CONF/unison.conf
touch $ODOO_CONF/unison.conf
echo "ODOO_PORT=$ODOO_PORT" >> $ODOO_CONF/unison.conf
echo "ADMIN_PWD=$ADMIN_PWD" >> $ODOO_CONF/unison.conf
echo "ODOO_LANGUAGE=$ODOO_LANGUAGE" >> $ODOO_CONF/unison.conf

# Start Odoo container (publish port 22 to allow remote debugging)
docker start odoo

# Container only starts sshd, no initialization yet

# Get private IP of Odoo
ODOO_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' odoo | tr -d '\n')

# Configure on Barman host to connect to Odoo (to copy filestore)
docker exec barman set-host odoo.local $ODOO_HOST

# Configure on Odoo host to connect to Aeroo
docker exec odoo set-host aeroo.local $AEROO_HOST

# Configure on Odoo host to connect to Postgresql
docker exec odoo set-host pgsql.local $PGSQL_HOST

# Configure and start Odoo
docker exec odoo service odoo start

# Wait until the initialization of Odoo has finalized (including the automated installation of modules)
# We will check every 2 minutes that tables have been created and the number of tables didn't increased (installation finalized)
TABLES_CURRENT=0
TABLES_LAST=0
QUERY="SELECT table_catalog, count(*) FROM information_schema.tables GROUP BY table_catalog"
while [ "$TABLES_CURRENT" == "0" ] || [ "$TABLES_CURRENT" != "$TABLES_LAST" ]; do
    sleep 120
    TABLES_LAST=$TABLES_CURRENT
    TABLES_CURRENT=`docker exec pgsql su postgres -c "psql -dodoo -c '$QUERY'" | grep odoo | cut -d '|' -f 2 | tr -d [:blank:]`
    echo "Current number of tables is $TABLES_CURRENT, last number of tables was $TABLES_LAST"
done

# Perform configuration of modules in the database
docker exec pgsql su postgres -c "psql -d odoo -c \"{CONFIG_SCRIPT}\""

###############################################
# Start NginX container (port 80 is offered
# just to force redirection to https)


# Several settings for NginX are stored on a file named params.conf
NGINX_PARAMS=$NGINX_CERTS/params.conf
echo "NGINX_PORT=$NGINX_PORT" > $NGINX_PARAMS

docker start nginx

# Create file with config values used by NginX
rm -rf $NGINX_CONF/unison.conf
touch $NGINX_CONF/unison.conf
echo "NGINX_PORT=$NGINX_PORT" >> $NGINX_CONF/unison.conf
echo "DNS_NAME=$DNS_NAME" >> $NGINX_CONF/unison.conf
echo "ODOO_PORT=$ODOO_PORT" >> $NGINX_CONF/unison.conf
echo "REQUEST_TIMEOUT=$REQUEST_TIMEOUT" >> $NGINX_CONF/unison.conf

# Configure on NginX host to connect to Odoo (their backend)
docker exec nginx set-host odoo.local $ODOO_HOST

# Start NginX
docker exec nginx service nginx start

# Wait for initialization
sleep 15

# Get NginX private IP (not used)
NGINX_HOST=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' nginx | tr -d '\n')

if [ "$IS_TEST" == 0 ]; then
     # On production nodes we start cAdvisor to monitor performance
     docker start cadvisor
else
     # On test nodes we start phpPgAdmin to browse the database
     docker start phppgadmin
fi

###############################################
# Indicate that initialization has ended
echo "$DNS_NAME" > /root/initialized

echo "SUCCESS: Node bootstrap completed"

exit 0
