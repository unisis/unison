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

    # This function is used to copy a file remotely
    def copy(self, local_file, remote_file):
        # Prepare ssh requirements
        self.prepare_ssh()

        # Copy file
        key_path = self.key_path()
        command = "scp -i " + key_path + " " + local_file + " root@" + self.public_ip + ":" + remote_file
        self.run_command(command)

        return True

    # This function is used to run a command via ssh on this node and return their output
    # We use port 2222 for host SSH service, so port 22 is reserved for SSH on test installation (for remote debugging)
    def execute(self, command, port=2222):
        # Prepare ssh requirements
        self.prepare_ssh()

        # Configure SSH connection
        key_path = self.key_path()
        shell = spur.SshShell(
            hostname = self.public_ip,
            port = port,
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

    # This function returns the location of the ssh private key
    def key_path(self):
        home_path = os.getenv("HOME")
        key_path = home_path + "/.ssh/node-" + str(self.id)
        return key_path

    # This function is used to prepare the requirements needed to
    # execute a ssh or scp command (create private key and add known host)
    def prepare_ssh(self):
        # Ensure that private key is stored
        key_path = self.key_path()
        if not os.path.isfile(key_path):
            key_content = self.key_id.private_key
            with open(key_path,'w') as f:
                f.write(key_content)

        # Endure that private key has the right permissions
        self.run_command("chmod 600 " + key_path)

        # Ensure that known_host file exists
        home_path = os.getenv("HOME")
        known_hosts = home_path + "/.ssh/known_hosts"
        if not os.path.isfile(known_hosts):
            self.run_command("touch " + known_hosts)

        # Ensure that current key is added as known host
        self.run_command("ssh-keygen -R " + self.public_ip + " 1>2 2>/dev/null")
        self.run_command("ssh-keyscan -t rsa " + self.public_ip + " >> " + known_hosts)

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output
