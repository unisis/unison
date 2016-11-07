# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store types of jobs executed in an async way
# The Odoo cron jobs are performed using transactions and the risk of face a "concurrent update" error
# are very high if we perform monolithic processes which takes long time to finish (while they lock
# the database). That's why we register the processes on different steps executed one by one
class JobType(models.Model):
    _name = 'unison.job_type'
    _order = 'name'

    code = fields.Char('Code', required=True, index=True)
    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True)
    frequency = fields.Integer('Frequency Minutes', required=True, default=0)
    last_exec = fields.Datetime('Last Execution')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
