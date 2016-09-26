# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate which repositories should be cloned so their modules
# are available to be installed on certain installations (via their "code" snapshot)
class CodeRepo(models.Model):
    _name = 'unison.code_repo'
    _rec_name = 'id'
    _order = 'id'

    code_id = fields.Many2one('unison.code', 'Code', ondelete='restrict')
    branch_id = fields.Many2one('unison.branch', 'Branch', ondelete='restrict')
    commit = fields.Char('Commit', index=True)  # Leave empty to always update to the latest commit
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
