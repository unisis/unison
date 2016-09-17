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
     name = fields.Char('Name', required=True)
     content = fields.Char('Content', required=True)
     ttl = fields.Integer('TTL', required=True)
     domain_id = fields.Many2one('unison.domain', 'Domain', ondelete='restrict')
     notes = fields.Char('Notes')
     active = fields.Boolean('Active')
