# -*- coding: utf-8 -*-

from openerp import models, fields

class NodeStat(models.Model):
     _name = 'unison.node_stat'
     _order = 'date'

     node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
     date = fields.Datetime('Date')
     cpu_used = fields.Integer('CPU Used')
     mem_used = fields.Integer('RAM Used')
     disk_used = fields.Integer('Disk Used')
     transfer_used = fields.Integer('Transfer Used')
