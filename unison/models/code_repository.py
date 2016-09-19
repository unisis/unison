# -*- coding: utf-8 -*-

from openerp import models, fields

class CodeRepository(models.Model):
     _name = 'unison.code_repository'
     _rec_name = 'id'
     _order = 'id'

     code_id = fields.Many2one('unison.code', 'Code', ondelete='restrict')
     branch_id = fields.Many2one('unison.branch', 'Branch', ondelete='restrict')
     commit = fields.Char('Commit', required=True, index=True)
     sequence = fields.Integer('Sequence')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
