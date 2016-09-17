# -*- coding: utf-8 -*-

from openerp import models, fields

class Volume(models.Model):
     _name = 'unison.volume'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     size_gb = fields.Integer('Size GB', required=True)
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
     mount_point = fields.Char('Mount Point')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)

