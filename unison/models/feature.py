# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the features available on regions (datacenters)
class Feature(models.Model):
     _name = 'unison.feature'
     _rec_name = 'code'
     _order = 'code'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
