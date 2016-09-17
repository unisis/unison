# -*- coding: utf-8 -*-

from openerp import models, fields

class Domain(models.Model):
     _name = 'unison.domain'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True)
     active = fields.Boolean('Active')

     records = fields.One2many('unison.record', 'domain_id', 'Domain Records')
