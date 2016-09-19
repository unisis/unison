# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the data about Git repositories
class Repository(models.Model):
     _name = 'unison.repository'
     _rec_name = 'url' # This model doesn't have a field named 'name'
     _order = 'repository_type_id, url'

     url = fields.Char('Url', required=True, index=True)
     description = fields.Char('Description')
     repository_type_id = fields.Many2one('unison.repository_type', 'Repository Type', ondelete='restrict')
     clone_command = fields.Char('Clone Command', required=True)
     ssh_private_key = fields.Text('SSH Private Key')
     forked_from_url = fields.Char('Forked From Url')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
