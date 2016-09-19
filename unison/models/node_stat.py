# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store statistics about a node
class NodeStat(models.Model):
     _name = 'unison.node_stat'
     _order = 'date'

     node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
     date = fields.Datetime('Date')
     cpu_cores = fields.Integer('CPU Cores')
     cpu_used = fields.Integer('CPU Used')
     mem_mb = fields.Integer('RAM MB')
     mem_used = fields.Integer('RAM Used %')
     disk_mb = fields.Integer('Disk MB')
     disk_used = fields.Integer('Disk Used %')
     transfer_used = fields.Integer('Transfer Used %')
