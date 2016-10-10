# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store information about IP addresses 
# which can be reserved and assigned to different nodes
class FloatingIp(models.Model):
    _name = 'unison.floating_ip'
    _rec_name = 'address'
    _order = 'address'

    address = fields.Char('Address', required=True, index=True)
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
