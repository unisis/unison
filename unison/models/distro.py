# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to indicate the different distros (products) we offer to users
# However, some distros can be private (is_public = False) meaning that only the admin
# can requeste an installation of those distros. Private distros are used for internal
# projects (like Step or TodoLimpio) or for in-progress (beta) production distros (not
# released yet). When we have updated containers and we want create or update the image,
# the field custom_image_id should be cleared. Then, UniSon will automatically create
# a temporary node using stock_image_id as image, will execute prepare-image.sh and
# will save a new image (custom_image_id) which will be used on new installations.
class Distro(models.Model):
    _name = 'unison.distro'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Text('Description', required=True, index=True)
    is_public = fields.Boolean('Is Public')
    domain_id = fields.Many2one('unison.domain', 'Domain', ondelete='restrict')  # For example, edif.com.ar
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict', help='Region used to launch new nodes for this distro')
    stock_image_id = fields.Many2one('unison.image', 'Stock Image', ondelete='restrict', help='Standard base image provided by DigitalOcean used to run prepare-image.sh and create the Custom image used on installations')
    custom_image_id = fields.Many2one('unison.image', 'Custom Image', ondelete='restrict', help='Custom image (private snapshot) automatically created using a base image, used to launch new nodes for this distro')
    version_id = fields.Many2one('unison.version', 'Version for New Installations', ondelete='restrict')
    min_size_id = fields.Many2one('unison.size', 'Minimal Image Size', ondelete='restrict')
    min_volume_gb = fields.Integer('Minimal Volume GB')
    manual_config = fields.Text('Manual Configuration Instructions')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # This function returns the name of the image, based on the name of the distro
    def image_name(self):
        name = "image-" + self.name
        name = name.lower()
        name = name.replace(" ", "-")
        return name
    
