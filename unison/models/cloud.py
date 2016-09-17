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

     regions = fields.One2many('unison.region', 'cloud_id', 'Cloud Regions')
     images = fields.One2many('unison.image', 'cloud_id', 'Cloud Images')
     sizes = fields.One2many('unison.size', 'cloud_id', 'Cloud Sizes')
     keys = fields.One2many('unison.key', 'cloud_id', 'Cloud Keys')
