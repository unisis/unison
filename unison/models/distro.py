# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate the different distros (products) we offer to users
class Distro(models.Model):
    _name = 'unison.distro'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Text('Description', required=True, index=True)
    domain_id = fields.Many2one('unison.domain', 'Domain', required=True, ondelete='restrict')  # For example, edif.com.ar
    region_id = fields.Many2one('unison.region', 'Region', required=True, ondelete='restrict', help='Region used to launch new nodes for this distro')
    image_id = fields.Many2one('unison.image', 'Image', required=True, ondelete='restrict', help='Private snapshot used to launch new nodes for this distro')
    code_id = fields.Many2one('unison.code', 'Code Template', required=True, ondelete='restrict')
    min_size_id = fields.Many2one('unison.size', 'Minimal Size', required=True, ondelete='restrict')
    manual_steps = fields.Text('Manual Configuration Instructions')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

