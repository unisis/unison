# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store the log of actions provided by the cloud provider
class Action(models.Model):
    _name = 'unison.action'
    _order = 'id'
    _rec_name = 'id'

    code = fields.Char('Code') # DigitalOcean code
    type = fields.Char('Type', required=True, index=True)
    status = fields.Char('Status', required=True, index=True)
    date_start = fields.Char('Date Started')
    date_end = fields.Char('Date Completed')
    resource_type = fields.Char('Resource Type')
    resource_code = fields.Char('Resource Code')
    region_id = fields.Many2one('unison.region', 'Region', ondelete='restrict')
