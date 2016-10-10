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
        command = "compute region list"
        return self.run_doctl(command)

    @api.model
    def get_images(self):
        command = "compute image list"
        return self.run_doctl(command)

    @api.model
    def get_sizes(self):
        command = "compute size list"
        return self.run_doctl(command)

    @api.model
    def get_keys(self):
        command = "compute ssh-key list"
        return self.run_doctl(command)

    @api.model
    def get_nodes(self):
        command = "compute droplet list"
        return self.run_doctl(command)

    @api.model
    def get_volumes(self):
        command = "compute volume list"
        return self.run_doctl(command)

    @api.model
    def get_floating_ips(self):
        command = "compute floating-ip list"
        return self.run_doctl(command)

    @api.model
    def get_domains(self):
        command = "compute domain list"
        return self.run_doctl(command)

    @api.model
    def get_records(self, domain_name):
        command = "compute domain records list " + domain_name
        return self.run_doctl(command)

    @api.model
    def get_actions(self, after):
        command = "compute action list --after '" + after + "'"
        print command
        return self.run_doctl(command)

    # This function is used to run a doctl command using a json output
    # but returning the result as a Python list
    def run_doctl(self, command):
        output = self.run_command("/usr/bin/doctl " + command + " --output json")
        list = json.loads(output)
        return list

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output
