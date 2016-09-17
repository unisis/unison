# -*- coding: utf-8 -*-

from openerp import models, fields

class Key(models.Model):
     _name = 'unison.key'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     fingerprint = fields.Char('Fingerprint')
     public_key = fields.Text('Public Key')
     private_key = fields.Text('Private Key (Linux)')
     putty_key = fields.Text('Private Key (PuTTY)')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)