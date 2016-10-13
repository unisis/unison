# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the DNS domains we are hosting
class Domain(models.Model):
    _name = 'unison.domain'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
    ttl = fields.Integer('TTL', required=True, index=True)
    zone_file = fields.Text('Zone File', required=True, index=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    records = fields.One2many('unison.record', 'domain_id', 'Domain Records')
