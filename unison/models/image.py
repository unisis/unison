# -*- coding: utf-8 -*-

from openerp import models, fields

class Image(models.Model):
     _name = 'unison.image'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
