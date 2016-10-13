# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This class is used to store the different clouds used on UniSon (at this moment, only DigitalOcean is supported)
class Cloud(models.Model):
    _name = 'unison.cloud'
    _order = 'name'

    code = fields.Char('Code') # DigitalOcean code, assigned after create
    name = fields.Char('Name', required=True, index=True)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # One to many relationships
    regions = fields.One2many('unison.region', 'cloud_id', 'Cloud Regions')
    images = fields.One2many('unison.image', 'cloud_id', 'Cloud Images')
    sizes = fields.One2many('unison.size', 'cloud_id', 'Cloud Sizes')
    keys = fields.One2many('unison.key', 'cloud_id', 'Cloud Keys')

