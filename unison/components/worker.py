# -*- coding: utf-8 -*-

import os
import uuid
import datetime
import logging
import subprocess
import dateutil.parser as dateparser
from shutil import copyfile
from openerp import models, fields, osv, exceptions, api

_logger = logging.getLogger(__name__)
# This component is invoked regularly (see data/cron.xml for details) 
# to perform the asynchronous tasks requested (or scheduled) on UniSon
class Worker(models.Model):
    _name = 'unison.worker'
    _auto = False # This settings avoids the creation of a table 

    # This function is used to check if there are tasks related
    # to the lifecycle of installations that should be performed
    @api.model
    def install_tasks(self):
        print "UNISON: Checking Server tasks..."

        # Check if there are custom images that should be created
        distro = self.env['unison.distro']
        distros = distro.search([('custom_image_id', '=', None)])
        for distro in distros:
            if distro.stock_image_id.name == False:
                print "WARNING!!!: No base/custom image was indicated for distro " + distro.name
                continue

            server_name = "image-" + str(distro.id)

            # The new custom image for this distro should be created or it's in creation.
            # During the first stage, a new DigitalOcean droplet named image-<distro_id> is created and inserted in the database
            # When that node is up, the prepare-image.sh script is executed. So, the first step is know if the droplet exists.
            node = self.env['unison.node']
            nodes = node.search([('name', '=', server_name)])
            if len(nodes) == 0:
                print "UNISON: Creating custom image for " + distro.name + " using as base image " + distro.stock_image_id.name + "..."

                # As first step, we will select any SSH key to assign to the node that will be created
                # to create the image. Since this will be a temporary node (destroyed after save snapshot)
                # any SSH key that have their private key stored is ok for our purposes
                key = self.env['unison.key']
                keys = key.search([('private_key', '!=', '')])
                key = keys[0]

                # Load settings for new node
                size = distro.min_size_id
                image = distro.stock_image_id
                region = distro.region_id

                # Create node to create the image
                print "UNISON: Creating Node " + server_name
                digital_ocean = self.env['unison.digital_ocean']
                node = digital_ocean.create_node(server_name, size.code, image.code, region.code, key.fingerprint)
                node = node[0]
                node_code = node['id']
                node_status = node['status']

                # Insert node record
                node = self.env['unison.node']
                node = node.create({
                    'code': node_code,
                    'name': server_name,
                    'image_id': image.id,
                    'size_id': size.id,
                    'region_id': region.id,
                    'key_id': key.id,
                    'record_id': None,
                    'public_ip': None, # Is not available at creation time
                    'private_ip': None, # Is not available at creation time
                    'status': node_status,
                    'notes': '',
                    'active': True
                })
                print "UNISON: Node " + server_name + " was created"

                # That's all for now, once the node is active, the process will continue
            else:
                # The node was already created. Check if it's active
                node = nodes[0]
                if node.status == "active":
                    # Create remote directory where config files will be stored
                    unisis_dir = "/etc/unisis/"
                    node.execute("mkdir -p " + unisis_dir, 22)

                    # Get configurations
                    config = self.env['unison.config']
                    configs = config.search([])
                    config = configs[0]

                    # We will create a file named /etc/unisis/general.conf 
                    # including all the general configs used by scripts
                    local_file = self.get_temp_path()
                    with open(local_file,'w') as f:
                        f.write("PORT_NGINX=" + str(config.port_nginx) + '\n')
                        f.write("PORT_ODOO=" + str(config.port_odoo) + '\n')
                        f.write("PORT_PGSQL=" + str(config.port_pgsql) + '\n')
                        f.write("PORT_AEROO=" + str(config.port_aeroo) + '\n')
                        f.write("SMTP_HOST_NAME=" + config.smtp_host_name + '\n')
                        f.write("SMTP_PORT_NUMBER=" + str(config.smtp_port_number) + '\n')
                        f.write("SMTP_USER_NAME=" + config.smtp_user_name + '\n')
                        f.write("SMTP_USER_PWD=" + config.smtp_user_pwd + '\n')
                        f.write("SMTP_SENDER_ADDRESS=" + config.smtp_sender_address + '\n')
                        f.write("SMTP_ALERTS_RECIPIENT=" + config.smtp_alerts_recipient + '\n')
                        f.write("S3_ACCESS_KEY=" + config.s3_access_key + '\n')
                        f.write("S3_SECRET_KEY=" + config.s3_secret_key + '\n')
                        f.write("S3_BACKUPS_BUCKET=" + config.s3_backups_bucket + '\n')
                        f.write("DOCKERHUB_EMAIL=" + config.dockerhub_email + '\n')
                        f.write("DOCKERHUB_AUTH=" + config.dockerhub_auth + '\n')
                    node.copy(local_file, unisis_dir + "general.conf")
                    self.run_command("rm -rf " + local_file)

                    # Get local directory where image files are stored
                    current_dir = os.path.dirname(os.path.realpath(__file__))
                    image_dir = current_dir + "/../image/"

                    # Copy template files to node (/etc/unisis directory)
                    node.copy(image_dir + "config.json", unisis_dir + "config.json")
                    node.copy(image_dir + "monitrc", unisis_dir + "monitrc")
                    node.copy(image_dir + "sshd_config", unisis_dir + "sshd_config")
                    node.copy(image_dir + "sysctl.conf", unisis_dir + "sysctl.conf")
                    node.copy(image_dir + "rc.local", unisis_dir + "rc.local")

                    # Copy scripts to /root directory
                    node.copy(image_dir + "prepare-dirs.sh", "/root/prepare-dirs.sh")
                    node.copy(image_dir + "prepare-image.sh", "/root/prepare-image.sh")
                    node.copy(image_dir + "prepare-node.sh", "/root/prepare-node.sh")

                    # Run command to prepare image
                    # node.execute("/bin/bash /root/prepare-image.sh", 22)   DDDDDDDDDDDEEEEEEEEEEEEBBBBBBBBBBBUUUUUUUUUUUUUUGGGGGGGGGGGGGGGGG
                    print "UNISON: Launched preparation of " + server_name

        # Check if there are servers inserted or provisioning
        server = self.env['unison.server']
        servers = server.search([('status', '=', 'inserted')])
        for server in servers:
            print "UNISON: Provisioning server " + server.name
            # Indicate that we are provisioning
            server.write({
                 'status': 'provisioning',
            })

            # Prepare variables
            server_number = "00000" + str(server.id)
            server_name = "server-" + server_number[-5:]
            install = server.install_id
            distro = install.distro_id
            region = distro.region_id
            size = distro.min_size_id # Node is created using the smaller size allowed for this distro
            image = distro.image_id

            # If this server use a floating IP, create it if it's not assigned yet
            if not server.is_test and install_id.use_floating_ip and not install.floating_ip_id:
                print "UNISON: Creating Floating IP..."
                digital_ocean = self.env['unison.digital_ocean']
                floating_ip = digital_ocean.create_floating_ip(region.code)
                floating_ip = floating_ip[0]
                address = floating_ip['ip']
                floating_ip = self.env['unison.floating_ip']
                floating_ip = floating_ip.create({
                    'address': address,
                    'region_id': region.id,
                    'node_id': None,
                    'notes': '',
                    'active': True
                })
                server.write({
                    'floating_ip_id': floating_ip['id'],
                })

            # Create volume for server
            if not server.volume_id:
                print "UNISON: Creating Volume..."
                digital_ocean = self.env['unison.digital_ocean']
                volume = digital_ocean.create_volume(server_name, region.code, install.volume_gb)
                volume_code = volume[0]['id']
                volume = self.env['unison.volume']
                volume = volume.create({
                    'code': volume_code,
                    'name': server_name,
                    'size_gb': install.volume_gb,
                    'region_id': region.id,
                    'node_id': None,
                    'filesystem': None,
                    'mount_point': None,
                    'notes': '',
                    'active': True
                })
                server.write({
                    'volume_id': volume['id'],
                })
            
            if not server.node_id:
                # Create SSH key for server
                print "UNISON: Creating SSH Key..."
                key = self.env['unison.key']
                values = key.generate()
                key = key.create({
                    'code': "no-code", # It's assigned later, see below
                    'name': server_name,
                    'cloud_id': image.cloud_id.id,
                    'fingerprint': values['fingerprint'],
                    'private_key': values['private_key'],
                    'public_key': values['public_key'],
                    'putty_key': values['putty_key'],
                    'notes': '',
                    'active': True
                })

                # Save key into digitalocean (and write code to model)
                digital_ocean = self.env['unison.digital_ocean']
                do_key = digital_ocean.create_key(server_name, key.public_key)
                key_code = do_key[0]['id']
                key.write({
                    'code': key_code,
                })

                # Create node for server
                print "UNISON: Creating Node..."
                digital_ocean = self.env['unison.digital_ocean']
                node = digital_ocean.create_node(server_name, size.code, image.code, region.code, key.fingerprint)
                node = node[0]
                node_code = node['id']
                node_status = node['status']

                # Insert node record
                node = self.env['unison.node']
                node = node.create({
                    'code': node_code,
                    'name': server_name,
                    'image_id': image.id,
                    'size_id': size.id,
                    'region_id': region.id,
                    'key_id': key.id,
                    'record_id': None, # TO-DO ASSIGN IF MANAGE_DNS IS TRUE
                    'public_ip': None, # Is not available at creation time
                    'private_ip': None, # Is not available at creation time
                    'status': node_status,
                    'notes': '',
                    'active': True
                })
                server.write({
                    'node_id': node.id,
                })

        server = self.env['unison.server']
        servers = server.search([('status', '=', 'provisioning')])
        for server in servers:
            print "UNISON: Finalizing provisioning of server " + server.name

            # The following actions should be performed when the server is ready
            if server.node_id and server.node_id.status == 'active':
                # Attach volume to node
                node = server.node_id
                volume = server.volume_id
                if node.status == 'active' and not volume.node_id:
                    print "UNISON: Attaching Volume to Node..."
                    volume_code = server.volume_id.code
                    node_code = server.node_id.code
                    digital_ocean = self.env['unison.digital_ocean']
                    digital_ocean.attach_volume(volume_code, node_code)
                    volume.write({
                        'node_id': node.id,
                    })

                # If this volume is new, format it. 
                filesystem = "ext4"
                if not volume.filesystem:
                    print "UNISON: Formatting volume..."
                    command = "mkfs." + filesystem + " -F /dev/disk/by-id/scsi-0DO_Volume_" + server_name
                    node.execute(command)
                    volume.write({
                        'filesystem': filesystem,
                    })

                # Mount it if it's not mounted.
                if not volume.mount_point:
                    print "UNISON: Mounting Volume on Node..."
                    mount_point = "/mnt/vol"
                    node.execute("mkdir -p " + mount_point)
                    node.execute("mount -o discard,defaults /dev/disk/by-id/scsi-0DO_Volume_" + server_name + " " + mount_point)
                    node.execute("echo '/dev/disk/by-id/scsi-0DO_Volume_" + server_name + " " + mount_point + " " + filesystem + " defaults,nofail,discard 0 0' >> /etc/fstab")
                    volume.write({
                        'mount_point': mount_point,
                    })

                # Install the node if their requirements are ready
                if node.status == 'active' and volume.node_id and volume.filesystem and volume.mount_point:
                    # Indicate that we are installing
                    server.write({
                        'status': 'installing',
                    })

                    # Configure hostname
                    host_name = node.name + '.' + install.domain_id.name
                    node.execute("echo " + host_name + " > /etc/hostname")
                    node.execute("hostname " + host_name)

                    # Copy SSL certificate to production server
                    if not server.is_test and install.certificate_id:
                        # Copy private key of certificate
                        certificate = install.certificate_id
                        temp_file = "/tmp/" + str(install.id)
                        node.copy(temp_file, "/mnt/vol/unisis/cert/cert.key")

                        # Copy certificate (concatenating intermediate cert if exists)
                        cert_content = ""
                        if certificate.intermediate:
                            cert_content = certificate.intermediate
                        cert_content = cert_content + "\n" + certificate.certificate
                        with open(temp_file,'w') as f:
                            f.write(cert_content)
                        node.copy(temp_file, "/mnt/vol/unisis/cert/cert.crt")

                    current_dir = os.path.dirname(os.path.realpath(__file__))
                    image_dir = current_dir + "/../image/"
                    node.copy(image_dir + "install.sh", "/root/install.sh")
                    node.copy(image_dir + "install.sh", "/root/install.sh")

                    # Indicate that Odoo is starting
                    server.write({
                        'status': 'starting',
                    })

        # Check if servers starting their containers are already up/online
        server = self.env['unison.server']
        servers = server.search([('status', '=', 'starting')])
        for server in servers:
            print "Checking if server " + server.name + " has started..."
            # TO-DO Check Odoo status

        print "UNISON: Finalized server tasks"

    # This function returns a temporary file path
    def get_temp_path(self):
        filename = str(uuid.uuid4())
        path = "/tmp/" + filename
        return path

    # This function repala a text/variable on a file with a value
    def replace_variable(self, file_path, variable_name, variable_value):
        command = "sed -i " + file_path + " -e 's|" + variable_name + "|" + str(variable_value) + "|g'"
        print command
        self.run_command(command)

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output

