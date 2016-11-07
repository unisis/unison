# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the Jobs executed
class Job(models.Model):
    _name = 'unison.job'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    job_type_id = fields.Many2one('unison.job_type', 'Job Type', ondelete='restrict')
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    success = fields.Boolean('Success')
    active = fields.Boolean('Active', default=True)

