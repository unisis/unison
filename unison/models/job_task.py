# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the Job Taks to be executed
# "Parallel" means that this task can be started when their previous task
# (according to the 'sequence' field) hasn't finished yet.
class JobTask(models.Model):
    _name = 'unison.job_task'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    job_id = fields.Many2one('unison.job', 'Job', required=True, ondelete='restrict')
    sequence = fields.Integer('Sequence', required=True, index=True)
    parallel = fields.Boolean('Parallel', required=True, default=False)
    model = fields.Char('Model', required=True, index=True)
    function = fields.Char('Function', required=True, index=True)
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    success = fields.Boolean('Success')
    output = fields.Text('Output')
    active = fields.Boolean('Active', default=True)
