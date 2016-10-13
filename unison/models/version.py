# -*- coding: utf-8 -*-

import hashlib
from openerp import models, fields, api

# A version represents the exact configuration (snapshot) of a code base, indicating
# all the repos used, the selected branches and the commit of each branch. Also, a
# version includes optional database commands to be executed when a new installation
# is created using some version, and database commands to be executed to upgrade from
# the previous version to the newer version. 

# Each version name is composed by three numeric parts: 
# 1) Major number (indicates big improvements compared with previous major number) 
# 2) Minor number (indicates small improvements compared with previous minor number)
# 3) Revision number (indicates a patch for bugs, just to fix issues)

# Each version is assigned to a distro (shared code to deploy on all installations
# of such distro) or to an installation (custom code/modules to add just to that
# installation)

# The serialization field is a virtual/calculated field to be able to have a text
# representation of each version (repos deployed, modules installed, db scripts)
# which can be used as a handy summary or to compare two versions using a tool like
# meld to easily see the differences between each version.

class Version(models.Model):
    _name = 'unison.version'
    _order = 'name'

    distro_id = fields.Many2one('unison.distro', 'For Distro', ondelete='restrict')
    install_id = fields.Many2one('unison.install', 'For Install', ondelete='restrict')
    name = fields.Char('Name', required=True, index=True)  # Like 1.0.2
    major = fields.Integer('Major Number', required=True)
    minor = fields.Integer('Minor Number', required=True)
    revision = fields.Integer('Revision Number', required=True)
    description = fields.Char('Description', required=True, index=True)
    install_db_script = fields.Text('Install DB Script')
    upgrade_db_script = fields.Text('Upgrade DB Script')
    serialization = fields.Text('Serialization', compute='_compute_serialization') # Text representation of every repo+branch+commit+installed modules
    hash = fields.Char('Hash', index=True) # Hash obtained from the serialization text, to identify if 2 versions are the same or not
    notes = fields.Text('Notes')

    # One to Many relations
    version_repos = fields.One2many('unison.version_repo', 'version_id', 'Repos')
    version_modules = fields.One2many('unison.version_module', 'version_id', 'Modules')

    # This function calculates the serialization of the version.
    # It's updated if the db scripts or the config of repos/modules are changed
    @api.one
    @api.depends('install_db_script', 'upgrade_db_script', 'version_repos.commit', 'version_modules.module_name')
    def _compute_serialization(self):
        serialization = 'Repositories:\n'
        for version_repo in self.version_repos:
             serialization = serialization + version_repo.branch_id.repo_id.url + '/' + version_repo.branch_id.name + '\n'

        serialization = serialization + '\nModules:\n'
        for version_module in self.version_modules:
             module_version = ''
             if version_module.version != False:
                 module_version = version_module.version
             serialization = serialization + version_module.module_name + '/' + module_version + '\n'

        serialization = serialization + '\nInstall DB Script:\n'
        install_db_script = ''
        if self.install_db_script != False:
             install_db_script = self.install_db_script
        serialization = serialization + install_db_script + '\n'

        serialization = serialization + '\nUpgrade DB Script:\n'
        upgrade_db_script = ''
        if self.upgrade_db_script != False:
             upgrade_db_script = self.upgrade_db_script
        serialization = serialization + upgrade_db_script + '\n'

        # Save hash of serialization
        md5 = hashlib.md5()
        md5.update(serialization)
        self.write({
            'hash': md5.hexdigest(),
        })

        self.serialization = serialization
