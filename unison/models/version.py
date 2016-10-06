# -*- coding: utf-8 -*-

from openerp import models, fields

# A version represents the exact configuration (snapshot) of a code base, indicating
# all the repos used, the selected branches and the commit of each branch. Also, a
# version includes optional database commands to be executed when a new installation
# is created using some version, and database commands to be executed to upgrade from
# the previous version to the newer version. Each version name is composed by three
# parts: 
# 1) Major number (indicates big improvements compared with previous major number) 
# 2) Minor number (indicates small improvements compared with previous minor number)
# 3) Revision number (indicates a patch for bugs, just to fix issues)
# Each version is assigned to a distro (shared code to deploy on all installations
# of such distro) or to an installation (custom code/modules to add just to that
# installation)
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
    notes = fields.Text('Notes')
