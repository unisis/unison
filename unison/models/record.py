# -*- coding: utf-8 -*-

from openerp import models, fields

class Record(models.Model):
     _name = 'unison.record'
     _order = 'name'

     types = [
         ('a', 'A'),
         ('cname', 'CNAME'),
         ('mx', 'MX'),
     ]

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     type = fields.Selection(types, 'Type')
     name = fields.Char('Name', required=True, index=True)
     content = fields.Char('Content', required=True, index=True)
     ttl = fields.Integer('TTL', required=True, help='Time To Live')
     domain_id = fields.Many2one('unison.domain', 'Domain', ondelete='restrict')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)

     # Reverse relationships
     nodes = fields.One2many('unison.node', 'record_id', 'Nodes')
