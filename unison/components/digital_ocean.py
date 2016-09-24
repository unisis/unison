# -*- coding: utf-8 -*-

import json
import logging
import subprocess

from openerp import models, fields, osv, exceptions

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

    def get_droplets_list(self, cr, uid):
        command = "/usr/bin/doctl compute droplet list --output json"
        return self.run_command(command)

    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        list = json.loads(output)
        for item in list:
            _logger.warning(item)
        return output
