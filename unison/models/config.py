# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store UniSon configurations. Odoo have their own mechanisms to store module settings,
# but I prefer keep the things simple and isolated, by creating a model to store the general configurations.
class Config(models.Model):
     _name = 'unison.config'
     _rec_name = 'id'
     _order = 'id'

     main_domain = fields.Char('Main Domain')
     region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict', help='Region from cloud were new nodes will be launched')
     snapshot_code = fields.Char('Snapshot', help='Snapshot Id used to launch nodes on the above region')
     notes = fields.Text('Notes')
