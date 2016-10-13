# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the different repository groups
class RepoGroup(models.Model):
    _name = 'unison.repo_group'
    _order = 'sequence'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True)
    url = fields.Char('Url')
    sequence = fields.Integer('Sequence')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
