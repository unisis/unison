# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This table is used to store the volumes which can be live without a node
# and can be mounted on different nodes (just one at the same time)
class Volume(models.Model):
    _name = 'unison.volume'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    size_gb = fields.Integer('Size GB', required=True)
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    filesystem = fields.Char('Filesystem')
    mount_point = fields.Char('Mount Point')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

