# -*- coding: utf-8 -*-

from openerp import models, fields

class RepositoryType(models.Model):
     _name = 'unison.repository_type'
     _order = 'sequence'

     code = fields.Char('Code', required=True)
     name = fields.Char('Name', required=True, index=True)
     description = fields.Char('Description', required=True)
     sequence = fields.Integer('Sequence')
