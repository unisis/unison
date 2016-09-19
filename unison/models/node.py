# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store information about cloud nodes 
# (host machines launched by UniSon)
class Node(models.Model):
     _name = 'unison.node'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     image_id = fields.Many2one('unison.image', 'Image', ondelete='restrict')
     size_id = fields.Many2one('unison.size', 'Size', ondelete='restrict')
     region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict')
     key_id = fields.Many2one('unison.key', 'Key', ondelete='restrict')
     record_id = fields.Many2one('unison.record', 'Record', ondelete='restrict')
     public_ip = fields.Char('Public IP')
     private_ip = fields.Char('Private IP')
     status = fields.Char('Status')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
