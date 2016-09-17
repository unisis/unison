# -*- coding: utf-8 -*-

from openerp import models, fields

class Branch(models.Model):
     _name = 'unison.branch'
     _order = 'name'

     name = fields.Char('Name', required=True, index=True)
     repository_id = fields.Many2one('unison.repository', 'Repository', ondelete='restrict')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
