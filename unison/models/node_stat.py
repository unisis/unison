# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store statistics about a node.
# cpu_cores, mem_db and disk_gb shows the total current capacity of the node (disk is referred to the data volume)
# cpu_used, mem_used and disk_used indicates the percentage of use of each resource
class NodeStat(models.Model):
     _name = 'unison.node_stat'
     _order = 'date'

     node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
     date = fields.Datetime('Date')
     cpu_cores = fields.Integer('CPU Cores')
     cpu_used = fields.Integer('CPU Used')
     mem_mb = fields.Integer('RAM MB')
     mem_used = fields.Integer('RAM Used %')
     disk_gb = fields.Integer('Disk GB')
     disk_used = fields.Integer('Disk Used %')
     transfer_used = fields.Integer('Transfer Used %')
