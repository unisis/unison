# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the different repository types (origins).
# Code values are shown on the provided constants
class RepositoryType(models.Model):
     _name = 'unison.repository_type'
     _order = 'sequence'

     ODOO_CODE = 0
     ODOO_ADDONS = 1
     OCA_ADDONS = 2
     ADHOC_ADDONS = 3
     UNISIS_ADDONS = 4
     CLIENT_ADDONS = 5

     code = fields.Char('Code', required=True)
     name = fields.Char('Name', required=True, index=True)
     description = fields.Char('Description', required=True)
     sequence = fields.Integer('Sequence')
