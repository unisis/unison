# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the node sizes available
class Size(models.Model):
    _name = 'unison.size'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
    ram_mb = fields.Integer('RAM MB')
    cpu_cores = fields.Integer('CPU Cores')
    disk_gb = fields.Integer('Disk GB')
    transfer_tb = fields.Integer('Transfer TB')
    hourly_price_usd = fields.Float('Hourly Price (USD)')
    available = fields.Boolean('Available', default=True, help='Available to create new droplets, setting provided by DigitalOcean')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # Reverse relationships
    nodes = fields.One2many('unison.node', 'size_id', 'Nodes')

    # The same node size is available on several regions (many to many)
    region_ids = fields.Many2many('unison.region', 'size_region_rel', 'size_id', 'region_id', string='Regions')
