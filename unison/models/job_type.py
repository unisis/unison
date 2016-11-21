# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store types of jobs executed on the background.
# See unisis.odt document for detailed documentation about the tables job_type, job and job_tasks.
# A new job can be triggered/generated in 3 ways:
# 1) When a specific event occurs on a model (trigger_model + trigger_event fields)
# 2) When a new period of minutes is completed since last job for a model (trigger_model + trigger_frequency)
# 3) Manually triggered (both trigger_event and trigger_frequency fields are empty)
# For example, on models like "image" and "install" the insert or delete of a record will trigger several tasks
# On models like node a task could be executed every some number of minutes just to perform a health check etc
# On other models like "restore", this operation could be only triggered manually
class JobType(models.Model):
    _name = 'unison.job_type'
    _order = 'name'

    code = fields.Char('Code', required=True, index=True)
    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True)
    trigger_model = fields.Char('Trigger Model')
    trigger_event = fields.Char('Trigger Event', default="insert")
    trigger_frequency = fields.Integer('Trigger Frequency (Minutes)', default=0)
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
