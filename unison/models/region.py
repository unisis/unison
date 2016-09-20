# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the cloud regions (datacenters)
class Region(models.Model):
     _name = 'unison.region'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean slug, assigned after create
     name = fields.Char('Name', required=True, index=True)
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     available = fields.Boolean('Available', default=True, help='Available to create new droplets, setting provided by DigitalOcean')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)

     # Reverse relationships
     nodes = fields.One2many('unison.node', 'region_id', 'Nodes')

     # Many2many relations fully defined on size, image and feature models, here we are defining the "inverse" relation
     size_ids = fields.Many2many('unison.size', string='Sizes')
     image_ids = fields.Many2many('unison.image', string='Images')
     feature_ids = fields.Many2many('unison.feature', string='Features')
