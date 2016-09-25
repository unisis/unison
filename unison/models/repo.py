# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the data about Git repositories
class Repo(models.Model):
    _name = 'unison.repo'

    types = [
        ('git', 'Git'),
        ('mercurial', 'Mercurial'),
    ]

    name = fields.Char('Name') # This is the repo name, will be added as suffix to the repo_group.url
    repo_group_id = fields.Many2one('unison.repo_group', 'Repository Group', ondelete='restrict')
    description = fields.Char('Description')
    core_code = fields.Boolean('Core Code', default=False) # True to indicate an Odoo core repo (which have addons on their ./addons subirectory)
    type = fields.Selection(types, 'Type', default='git')
    is_private = fields.Boolean('Is Private', default=False)
    ssh_private_key = fields.Text('SSH Private Key')
    fork_repo_id = fields.Many2one('unison.repo', 'Forked Repo', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
