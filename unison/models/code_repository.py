# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate which repositories should be cloned so their modules
# are available to be installed on certain installations (via their "code" snapshot)
class CodeRepository(models.Model):
    _name = 'unison.code_repository'
    _rec_name = 'id'
    _order = 'sequence'

    code_id = fields.Many2one('unison.code', 'Code', ondelete='restrict')
    branch_id = fields.Many2one('unison.branch', 'Branch', ondelete='restrict')
    commit = fields.Char('Commit', required=True, index=True)
    sequence = fields.Integer('Sequence')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
