# -*- coding: utf-8 -*-

import os
import spur
import string
import subprocess
from openerp import models, fields, api

# This model is used to store information about cloud nodes 
# (host machines launched by UniSon)
class Node(models.Model):
    _name = 'unison.node'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    image_id = fields.Many2one('unison.image', 'Image', ondelete='restrict')
    size_id = fields.Many2one('unison.size', 'Size', ondelete='restrict')
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict')
    key_id = fields.Many2one('unison.key', 'Key', ondelete='restrict')
    record_id = fields.Many2one('unison.record', 'Record', ondelete='restrict')
    public_ip = fields.Char('Public IP')
    private_ip = fields.Char('Private IP')
    status = fields.Char('Status')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # This function is used to run a command via ssh on this node and return their output
    def execute(self, command):
        # Ensure that private key is stored
        home_path = os.getenv("HOME")
        key_path = home_path + "/.ssh/node-" + str(self.id)
        if not os.path.isfile(key_path):
            key_content = self.key_id.private_key
            with open(key_path,'w') as f:
                f.write(key_content)
            self.run_command("chmod 600 " + key_path)

        # Ensure that host is trusted as a known host
        known = self.run_command("ssh-keygen -F " + self.public_ip)
        if not known:
            print "Adding to known hosts " + self.public_ip
            self.run_command("ssh-keyscan -H " + self.public_ip + " >> " + home_path + "/.ssh/known_hosts")

        # Use a private key
        shell = spur.SshShell(
            hostname = self.public_ip,
            port = 22,
            username = "root",
            private_key_file = key_path,
            connect_timeout = 30,
            load_system_host_keys = True,
            look_for_private_keys = False
        )

        # Command should be provided as an array
        args = string.split(command, " ")

        try:
            result = shell.run(args)
            output = result.output
        except ValueError:
            print "ERROR: " + command
            output = ""

        return output

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output
