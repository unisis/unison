# Image Files

These files should be used to manually build a new image on a droplet

Procedure:

1 - Manually create a DigitalOcean droplet on the selected region using the Ubuntu 16.04 image
2 - Copy all the files included on this directory to the /root directory on that droplet
3 - Execute /bin/bash install.sh
4 - This is an interactive script, you will be asked to type the Docker Hub credentials, the Amazon S3 credentials etc
5 - Create a snapshot of the created droplet.
6 - On UniSon, on the Distro configuration, configure the name of the created snapshot
