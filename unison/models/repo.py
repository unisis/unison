# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the data about Git repositories
class Repo(models.Model):
    _name = 'unison.repo'
    _order = 'name'

    types = [
        ('git', 'Git'),
        ('mercurial', 'Mercurial'),
    ]

    name = fields.Char('Name') # This is the repo name, will be added as suffix to the repo_group.url
    url = fields.Char('Url', compute='_compute_url')
    repo_group_id = fields.Many2one('unison.repo_group', 'Repository Group', ondelete='restrict')
    description = fields.Char('Description')
    is_main = fields.Boolean('Is Main', default=False) # True to indicate an Odoo main repo (which have addons on their ./addons subirectory)
    type = fields.Selection(types, 'Type', default='git')
    is_private = fields.Boolean('Is Private', default=False)
    clone_command = fields.Text('Clone Command') # Only required for private repos
    ssh_private_key = fields.Text('SSH Private Key')
    fork_repo_id = fields.Many2one('unison.repo', 'Forked Repo', ondelete='restrict')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # This function calculates the url of the current repo. 
    # It's recalculated if the name or repo_group_id fields changes
    @api.one
    @api.depends('name', 'repo_group_id')
    def _compute_url(self):
        if len(self.repo_group_id) == 0:
            repo_group_url = ''
        else:
            repo_group_url = self.repo_group_id.url
        if self.name == False:
            repo_name = ''
        else:
            repo_name = self.name
        self.url = repo_group_url + '/' + repo_name

