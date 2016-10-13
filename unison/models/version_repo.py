# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to indicate which repositories should be cloned so their modules
# are available to be installed on certain installations (via their "version" snapshot)
# branch_id identifies their repository.
class VersionRepo(models.Model):
    _name = 'unison.version_repo'
    _rec_name = 'id'
    _order = 'id'

    version_id = fields.Many2one('unison.version', 'Version', required=True, ondelete='restrict')
    branch_id = fields.Many2one('unison.branch', 'Branch', required=True, ondelete='restrict')
    commit = fields.Char('Commit', index=True) # This field should be required, but first time a repo is added, is empty (later this field is automatically populated)
