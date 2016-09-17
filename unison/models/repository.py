# -*- coding: utf-8 -*-

from openerp import models, fields

class Repository(models.Model):
     _name = 'unison.repository'
     _order = 'repository_type_id, url'

     url = fields.Char('Url', required=True, index=True)
     description = fields.Char('Description')
     repository_type_id = fields.Many2one('unison.repository_type', 'Repository Type', ondelete='restrict')
     clone_command = fields.Char('Clone Command', required=True)
     ssh_private_key = fields.Text('SSH Private Key')
     forked_from_url = fields.Char('Forked From Url')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
