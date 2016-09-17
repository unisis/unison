# -*- coding: utf-8 -*-

from openerp import models, fields

class RepositoryType(models.Model):
     _name = 'unison.repository_type'
     _order = 'name'

     code = fields.Char('Code', required=True)
     name = fields.Char('Name', required=True)
     description = fields.Char('Description', required=True)
