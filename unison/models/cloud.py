# -*- coding: utf-8 -*-

from openerp import models, fields

class Cloud(models.Model):
     _name = 'unison.cloud'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     api_key = fields.Char('API Key', required=True, help='API Key used to automated operations')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)

     # records = fields.One2many('unison.record', 'domain_id', 'Domain Records')
