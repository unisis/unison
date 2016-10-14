# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to indicate the different distros (products) we offer to users
# However, some distros can be private (is_public = False) meaning that only the admin
# can requeste an installation of those distros. Private distros are used for internal
# projects (like Step or TodoLimpio) or for in-progress (beta) production distros (not
# released yet)
class Distro(models.Model):
    _name = 'unison.distro'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Text('Description', required=True, index=True)
    is_public = fields.Boolean('Is Public')
    domain_id = fields.Many2one('unison.domain', 'Domain', ondelete='restrict')  # For example, edif.com.ar
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict', help='Region used to launch new nodes for this distro')
    image_id = fields.Many2one('unison.image', 'Image', ondelete='restrict', help='Private snapshot used to launch new nodes for this distro')
    version_id = fields.Many2one('unison.version', 'Version for New Installations', ondelete='restrict')
    min_size_id = fields.Many2one('unison.size', 'Minimal Image Size', ondelete='restrict')
    min_volume_gb = fields.Integer('Minimal Volume GB')
    manual_config = fields.Text('Manual Configuration Instructions')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

