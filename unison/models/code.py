# -*- coding: utf-8 -*-

from openerp import models, fields

# Code represents the exact configuration of code for a distro template. Also, when a new
# installation is created, if some change is performed on a code config, a copy is created
# It's like a "super-commit" hash, but not related to just one repository, it's related to the
# entire configuration of all added repositories, their selected branches and the commits on each branch
# Just one of the selected repos should have repo.only_addons=0 (meaning that contains the Odoo code base)
# Therefore, code represents a snapshot of the code at certain exact point. The code_id field is to provide
# some kind of "inheritance" so we can configure a set of repos and modules and then use that definition
# (pointing to their code record) and just extend/add the extra repos and modules (without re-define all again)
class Code(models.Model):
    _name = 'unison.code'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description')
    default_branch = fields.Char('Default Branch', default='8.0')
    code_id = fields.Many2one('unison.code', 'Extended Code', ondelete='restrict')
    hash = fields.Char('Code Hash', index=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
