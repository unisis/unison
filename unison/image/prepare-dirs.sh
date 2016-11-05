#!/bin/bash

# This script is used to prepare the different directories used
# to store data that will be mounted on different containers

# NOTE: Do not place "exit 0" at the end of this script, because
# this script is sourced (executed on same subshell). Otherwise
# it will stop the execution of the caller script.

BASEDIR=/mnt/vol/unisis

BARMAN_CONF=$BASEDIR/barman/conf
BARMAN_DATA=$BASEDIR/barman/data
BARMAN_LOGS=$BASEDIR/barman/logs

PGSQL_CONF=$BASEDIR/pgsql/conf
PGSQL_DATA=$BASEDIR/pgsql/data
PGSQL_LOGS=$BASEDIR/pgsql/logs

NGINX_CONF=$BASEDIR/nginx/conf
NGINX_CERT=$BASEDIR/nginx/cert
NGINX_LOGS=$BASEDIR/nginx/logs

ODOO_ADDONS=$BASEDIR/odoo/addons
ODOO_CONF=$BASEDIR/odoo/conf
ODOO_DATA=$BASEDIR/odoo/data
ODOO_LOGS=$BASEDIR/odoo/logs
ODOO_SOURCE=$BASEDIR/odoo/source

ODOO_SSH=$ODOO_DATA/.ssh
PGSQL_SSH=$PGSQL_DATA/.ssh
BARMAN_SSH=$BARMAN_DATA/.ssh

# Check if a new volume is mounted on /mnt/vol
# In that case, define the mount points
if [ ! -d $BASEDIR ]; then
    # Define host mounts for volumes
    mkdir -p $BARMAN_DATA
    mkdir -p $BARMAN_LOGS

    mkdir -p $PGSQL_DATA
    mkdir -p $PGSQL_LOGS

    mkdir -p $NGINX_CERT
    mkdir -p $NGINX_LOGS

    mkdir -p $ODOO_ADDONS
    mkdir -p $ODOO_CONF
    mkdir -p $ODOO_DATA
    mkdir -p $ODOO_LOGS
    mkdir -p $ODOO_SOURCE

    chmod 777 -R $BASEDIR

    # Will copy the SSH key created for this droplet to be used on odoo, postgres and barman
    # so barman can communicate via SSH with Odoo (to backup their files) and Postgres (to backup their wal files)
    # Home dirs (in their containers) are /var/lib/odoo, /var/lib/postgresql and /var/lib/barman
    if [ -e /root/.ssh/id_rsa ]; then
        mkdir -p $ODOO_SSH
        mkdir -p $PGSQL_SSH
        mkdir -p $BARMAN_SSH

        cp /root/.ssh/id_rsa* $ODOO_SSH/
        cp /root/.ssh/id_rsa* $PGSQL_SSH/
        cp /root/.ssh/id_rsa* $BARMAN_SSH/

        cp /root/.ssh/id_rsa.pub $ODOO_SSH/authorized_keys
        cp /root/.ssh/id_rsa.pub $PGSQL_SSH/authorized_keys
        cp /root/.ssh/id_rsa.pub $BARMAN_SSH/authorized_keys
    fi
fi
