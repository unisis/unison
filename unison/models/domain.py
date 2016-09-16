# -*- coding: utf-8 -*-

from openerp import models, fields

class Domain(models.Model):
     _name = 'unison.domain'

     code = fields.Char('Code', required=True)
     name = fields.Char('Name', required=True)
     active = fields.Boolean('Active')
