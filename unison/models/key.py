# -*- coding: utf-8 -*-

import uuid
import subprocess
from openerp import models, fields, api

# This model is used to store information about SSH keys generated by us,
# which sometimes are uploaded to cloud providers to access the nodes.
# So, sometimes code and cloud_id will be null (if key was not uploaded)
class Key(models.Model):
    _name = 'unison.key'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
    fingerprint = fields.Char('Fingerprint')
    public_key = fields.Text('Public Key')
    private_key = fields.Text('Private Key (Linux)')
    putty_key = fields.Text('Private Key (PuTTY)')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [
        ('fingerprint_uniq', 'unique(fingerprint)', 'A key with same fingerprint exists'),
    ]

    # Reverse relationships
    nodes = fields.One2many('unison.node', 'key_id', 'Nodes')

    # This function generates a new SSH Key and loads the values in the temp model
    def generate(self):
        temp_file = self.get_temp_path()

        self.run_command("rm -rf " + temp_file + "*")
        self.run_command("ssh-keygen -t rsa -b 4096 -f " + temp_file + " -N ''")

        private_key = self.read_file(temp_file)
        public_key = self.read_file(temp_file + ".pub")

        fingerprint = self.run_command("ssh-keygen -lf " + temp_file + ".pub | cut -d ' ' -f 2")
        fingerprint = fingerprint.replace("\n", "")

        # Create putty version (.ppk) for Windows users
        putty_file = temp_file + ".ppk"
        self.run_command("rm -rf " + putty_file)
        self.run_command("puttygen " + temp_file + " -o " + putty_file)
        putty_key = self.read_file(putty_file)

        # Return values in a dictionary
        return {'fingerprint': fingerprint, 'private_key': private_key, 'public_key': public_key, 'putty_key': putty_key}

    # This function is used to run a shell command and return their output
    def run_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = process.stdout.read()
        return output

    # This function reads the content of a file
    def read_file(self, file_path):
        return self.run_command("cat " + file_path)

    # This function returns a temporary file path
    def get_temp_path(self):
        filename = str(uuid.uuid4())
        path = "/tmp/" + filename
        return path
