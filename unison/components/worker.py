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

            # Create floating IP for installation
            if install.use_floating_ip and not install.floating_ip_id:
                print "Creating Floating IP..."
                digital_ocean = self.env['unison.digital_ocean']
                region = install.distro_id.region_id
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

        print "UNISON: Finalized Installation tasks"

