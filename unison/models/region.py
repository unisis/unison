# -*- coding: utf-8 -*-

from openerp import models, fields

class Region(models.Model):
     _name = 'unison.region'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     features = fields.Text('Features')
     available = fields.Boolean('Available', default=True, help='Available to create new droplets, setting provided by DigitalOcean')
     selectable = fields.Boolean('Selectable', default=True, help='Indicates if we will launch droplets on this region, setting provided by UniSis')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
