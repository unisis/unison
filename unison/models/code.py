# -*- coding: utf-8 -*-

from openerp import models, fields

# Code represents the exact configuration of code for an installation or template
# It's like a "super-commit" hash, but not related to just one repository, it's related to the
# entire configuration of all added repositories, their selected branches and the commits on each branch
# Therefore, code represents a snapshot of the code at certain exact point
class Code(models.Model):
     _name = 'unison.code'
     _rec_name = 'hash'
     _order = 'hash'

     hash = fields.Char('Code Hash', required=True, index=True)
     description = fields.Char('Description')
     is_template = fields.Boolean('Is Template?')
     manual_config = fields.Text('Manual Configuration')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)
