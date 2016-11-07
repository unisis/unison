# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store each Job step
class JobStep(models.Model):
    _name = 'unison.job_step'
    _order = 'job_id, sequence'

    name = fields.Char('Name', required=True, index=True)
    job_id = fields.Many2one('unison.job', 'Job', ondelete='restrict')
    sequence = fields.Integer('Sequence', required=True, index=True)
    model = fields.Char('Model', required=True, index=True)
    function = fields.Char('Function', required=True, index=True)
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    success = fields.Boolean('Success')
    output = fields.Text('Output')
    active = fields.Boolean('Active', default=True)

