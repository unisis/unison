# -*- coding: utf-8 -*-

from openerp import models, fields

# This model store the branches defined on each Git repository
class Branch(models.Model):
    _name = 'unison.branch'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    repo_id = fields.Many2one('unison.repo', 'Repository', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
