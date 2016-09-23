# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store information about IP addresses 
# which can be reserved and assigned to different nodes
class FloatIp(models.Model):
    _name = 'unison.float_ip'
    _rec_name = 'address'
    _order = 'address'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    address = fields.Char('Address', required=True, index=True)
    cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    date_attach = fields.Datetime('Date Attach')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
