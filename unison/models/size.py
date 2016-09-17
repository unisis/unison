# -*- coding: utf-8 -*-

from openerp import models, fields

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
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
