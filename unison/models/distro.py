# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate the different distros (products) we offer to users
class Distro(models.Model):
    _name = 'unison.distro'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Text('Description', required=True, index=True)
    domain_id = fields.Many2one('unison.domain', 'Domain', required=True, ondelete='restrict')  # For example, edif.com.ar
    code_id = fields.Many2one('unison.code', 'Code Template', required=True, ondelete='restrict')
    manual_steps = fields.Text('Manual Configuration Instructions')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
