# -*- coding: utf-8 -*-

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

# The fields repos_conf and modules_conf are virtual/calculated fields which includes
# a text (denormalized) representation of the repos to be deployed and the modules to
# be installed (detailed on the version_repo and version_module tables). These fields
# are used to easily compare differences between versions using a tool like meld, 
# but they are also used to provide a text-based configuration which will be used 
# by the Odoo container to know which repos clone and which modules install before 
# start the Odoo service.

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
    repos_conf = fields.Text('Repos Conf', compute='_compute_repos_conf') # Text representation of every repo to clone (repo+branch+commit)
    modules_conf = fields.Text('Modules Conf', compute='_compute_modules_conf') # Text representation of every module name to install
    date_released = fields.Datetime('Date Released') # When the version was considered ready for production use (after finish the tests)
    notes = fields.Text('Notes')

    # One to Many relations
    version_repos = fields.One2many('unison.version_repo', 'version_id', 'Repos')
    version_modules = fields.One2many('unison.version_module', 'version_id', 'Modules')

    # This function calculates the serialization of the repos_conf field
    # It's updated if the config of the repos is changed
    @api.one
    @api.depends('version_repos.commit')
    def _compute_repos_conf(self):
        repos_conf = ""
        for version_repo in self.version_repos:
             repo_commit = ''
             if version_repo.commit != False:
                 repo_commit = version_repo.commit
             repos_conf = repos_conf + version_repo.branch_id.repo_id.url + '|' + version_repo.branch_id.name + '|' + repo_commit + '\n'
        self.repos_conf = repos_conf

    # This function calculates the serialization of the modules_conf field
    # It's updated if the config of the modules is changed
    @api.one
    @api.depends('version_modules.module_name')
    def _compute_modules_conf(self):
        modules_conf = ""
        for version_module in self.version_modules:
             module_version = ''
             if version_module.version != False:
                 module_version = version_module.version
             modules_conf = modules_conf + version_module.module_name + '|' + module_version + '\n'
        self.modules_conf = modules_conf
