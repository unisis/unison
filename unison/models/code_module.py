# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate which modules should be automatically installed
# when a new installation is required
class CodeModule(models.Model):
     _name = 'unison.code_module'
     _rec_name = 'module_name'
     _order = 'module_name'

     code_id = fields.Many2one('unison.code', 'Code', ondelete='restrict')
     module_name = fields.Char('Module', required=True, index=True)
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
