# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the data about Git repositories
class Repo(models.Model):
    _name = 'unison.repo'

    types = [
        ('git', 'Git'),
        ('mercurial', 'Mercurial'),
    ]

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description')
    repo_group_id = fields.Many2one('unison.repo_group', 'Repository Group', ondelete='restrict')
    url = fields.Char('Url')
    only_addons = fields.Boolean('Only Addons', default=True) # False to indicate a Odoo installation which have addons on their ./addons subirectory
    type = fields.Selection(types, 'Type', default='git')
    is_private = fields.Boolean('Is Private', default=False)
    clone_command = fields.Char('Clone Command', required=True)
    ssh_private_key = fields.Text('SSH Private Key')
    fork_repo_id = fields.Many2one('unison.repo', 'Forked Repo', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
