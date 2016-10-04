# -*- coding: utf-8 -*-

from openerp import models, fields

# Code represents the exact configuration of code for an installation or distro template
# It's like a "super-commit" hash, but not related to just one repository, it's related to the
# entire configuration of all added repositories, their selected branches and the commits on each branch
# Just one of the selected repos should have repo.only_addons=0 (meaning that contains the Odoo code base)
# Therefore, code represents a snapshot of the code at certain exact point
class Code(models.Model):
    _name = 'unison.code'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description')
    hash = fields.Char('Code Hash', index=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
