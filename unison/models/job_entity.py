# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store the Entities (images, nodes, etc)
# created as part of a job to be referenced by several job steps
class JobEntity(models.Model):
    _name = 'unison.job_entity'
    _order = 'job_id, type, code'

    type = fields.Char('Type', required=True, index=True)
    job_id = fields.Many2one('unison.job', 'Job', ondelete='restrict')
    code = fields.Char('Code', required=True, index=True)
    role = fields.Char('Role') # This field could be used if a job creates more than 1 instance of the same entity type 
    active = fields.Boolean('Active', default=True)

