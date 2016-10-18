# -*- coding: utf-8 -*-

import json
import logging
import subprocess

from openerp import models, fields, osv, exceptions, api

_logger = logging.getLogger(__name__)

# This model is the service wrapper to perform operations on DigitalOcean
# It use the doctl command line utility under the hood (we assume that the
# doctl command is already installed and the DIGITALOCEAN_ACCESS_TOKEN
# variable was already exported for authentication purposes)
# The _auto property is configured to False to avoid the creation of a table
# This model doesn't offer properties, just functions
class DigitalOcean(models.Model):
    _name = 'unison.digital_ocean'
    _auto = False # This settings avoids the creation of a table 

    @api.model
    def get_regions(self):
        command = "region list"
        return self.run_doctl(command)

    @api.model
    def get_images(self):
        command = "image list"
        return self.run_doctl(command)

    @api.model
    def get_sizes(self):
        command = "size list"
        return self.run_doctl(command)

    @api.model
    def get_keys(self):
        command = "ssh-key list"
        return self.run_doctl(command)

    @api.model
    def get_nodes(self):
        command = "droplet list"
        return self.run_doctl(command)

    @api.model
    def get_volumes(self):
        command = "volume list"
        return self.run_doctl(command)

    @api.model
    def get_floating_ips(self):
        command = "floating-ip list"
        return self.run_doctl(command)

    @api.model
    def get_domains(self):
        command = "domain list"
        return self.run_doctl(command)

    @api.model
    def get_records(self, domain_name):
        command = "domain records list " + domain_name
        return self.run_doctl(command)

    @api.model
    def get_actions(self, after):
        command = "action list --after '" + after + "'"
        return self.run_doctl(command)

    @api.model
    def create_floating_ip(self, region_code):
        command = "floating-ip create --region " + region_code
        return self.run_doctl(command)

    @api.model
    def create_key(self, name, public_key):
        command = "ssh-key create " + name + " --public-key '" + public_key + "'"
        return self.run_doctl(command)

    @api.model
    def create_volume(self, name, region_code, size_gb):
        command = "volume create " + name + " --size " + str(size_gb) + "GiB --region " + region_code
        return self.run_doctl(command)

    @api.model
    def attach_volume(self, volume_code, node_code):
        command = "volume-action attach " + str(volume_code) + " " + str(node_code)
        return self.run_doctl(command)

    @api.model
    def detach_volume(self, volume_code):
        command = "volume-action detach " + str(volume_code)
        return self.run_doctl(command)

    @api.model
    def create_node(self, name, size_code, image_code, region_code, key_fingerprint=None):
        command = "droplet create " + name + " --size " + size_code + " --image " + image_code + " --region " + region_code
        if key_fingerprint != False:
            command = command + " --ssh-keys " + key_fingerprint
        return self.run_doctl(command)

    # This function is used to run a doctl command using a json output
    # but returning the result as a Python list
    def run_doctl(self, command):
        output = self.run_command("/usr/bin/doctl compute " + command + " --output json")
        try:
            list = json.loads(output)
        except ValueError:
            print "ERROR: " + output
            list = ""
        return list

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output
