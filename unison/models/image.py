# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store information about images stored by each Cloud provider
# This also includes custom images that we can prepare for our own needs.
class Image(models.Model):
    _name = 'unison.image'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    cloud_id = fields.Many2one('unison.cloud', 'Cloud', ondelete='restrict')
    is_backup = fields.Boolean('Is Backup')
    is_private = fields.Boolean('Is Private')
    min_disk_size = fields.Integer('Min Disk Size GB')
    distribution = fields.Char('Distribution')
    created_at = fields.Datetime('Created At')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # Reverse relationships
    nodes = fields.One2many('unison.node', 'image_id', 'Nodes')

    # The same node image is available on several regions (many to many)
    region_ids = fields.Many2many('unison.region', 'image_region_rel', 'image_id', 'region_id', string='Regions')
