# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the DNS records defined on DigitalOcean
class Record(models.Model):
    _name = 'unison.record'
    _order = 'name'

    # Record types supported by DigitalOcean DNS system
    types = [
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('CNAME', 'CNAME'),
        ('MX', 'MX'),
        ('NS', 'NS'),
        ('PTR', 'PTR'),
        ('SRV', 'SRV'),
        ('TXT', 'TXT'),
    ]

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    type = fields.Selection(types, 'Type')
    name = fields.Char('Name', required=True, index=True)
    content = fields.Char('Content', required=True, index=True)
    priority = fields.Integer('Priority')
    domain_id = fields.Many2one('unison.domain', 'Domain', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # Reverse relationships
    nodes = fields.One2many('unison.node', 'record_id', 'Nodes')
