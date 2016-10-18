# -*- coding: utf-8 -*-

import os
import datetime
import logging
import subprocess
import dateutil.parser as dateparser
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
        print "UNISON: Checking Installation tasks..."

        # Check if there are installations inserted (to be created)
        install = self.env['unison.install']
        installs = install.search([('status', '=', 'inserted')])
        for install in installs:
            print "UNISON: Provisioning installation " + install.name
            install_code = "00000" + str(install.id)
            install_name = "inst-" + install_code[-5:]
            distro = install.distro_id
            region = distro.region_id
            size = distro.min_size_id # Node is created using the smaller size allowed for this distro
            image = distro.image_id

            # If this installation use a floating IP, create it if it's not assigned yet
            if install.use_floating_ip and not install.floating_ip_id:
                print "Creating Floating IP..."
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
                install.write({
                    'floating_ip_id': floating_ip['id'],
                })

            # Create volume for installation
            if not install.volume_id:
                print "Creating Volume..."
                digital_ocean = self.env['unison.digital_ocean']
                volume = digital_ocean.create_volume(install_name, region.code, install.volume_gb)
                volume_code = volume[0]['id']
                volume = self.env['unison.volume']
                volume = volume.create({
                    'code': volume_code,
                    'name': install_name,
                    'size_gb': install.volume_gb,
                    'region_id': region.id,
                    'node_id': None,
                    'filesystem': None,
                    'mount_point': None,
                    'notes': '',
                    'active': True
                })
                install.write({
                    'volume_id': volume['id'],
                })
            
            if not install.node_id:
                # Create SSH key for installation
                print "Creating SSH Key..."
                key = self.env['unison.key']
                values = key.generate()
                key = key.create({
                    'code': "no-code", # It's assigned later, see below
                    'name': install_name,
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
                do_key = digital_ocean.create_key(install_name, key.public_key)
                key_code = do_key[0]['id']
                key.write({
                    'code': key_code,
                })

                # Create node for installation
                print "Creating Node..."
                digital_ocean = self.env['unison.digital_ocean']
                node = digital_ocean.create_node(install_name, size.code, image.code, region.code, key.fingerprint)
                node = node[0]
                node_code = node['id']
                node_status = node['status']

                # Insert node record
                node = self.env['unison.node']
                node = node.create({
                    'code': node_code,
                    'name': install_name,
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

                install.write({
                    'node_id': node.id,
                })

            # Attach volume to node when status is active
            node = install.node_id
            volume = install.volume_id
            if node.status == 'active' and volume.node_id == None:
                print "Attaching Volume to Node..."
                volume_code = install.volume_id.code
                node_code = install.node_id.code
                volume = digital_ocean.attach_volume(volume_code, node_code)
     
        print "UNISON: Finalized Installation tasks"
