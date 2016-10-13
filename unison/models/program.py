# -*- coding: utf-8 -*-

from openerp import models, fields, api

# Clients are able to program backups at different hours of the day on each week day
class Program(models.Model):
    _name = 'unison.program'
    _rec_name = 'id'
    _order = 'week_day, hour, minutes'

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    week_day = fields.Integer('Week Day')
    hour = fields.Integer('Hour')
    minutes = fields.Integer('Minutes')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
