# -*- coding: utf-8 -*-

from openerp import models, fields

# We provide support for "intermitent" use of installations (just certain hours of the day)
# This model is used to schedule which hours the node should be running each week day
class Schedule(models.Model):
    _name = 'unison.schedule'
    _rec_name = 'week_day'
    _order = 'week_day'

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    week_day = fields.Integer('Week Day')
    start_hour = fields.Integer('Start Hour')
    end_hour = fields.Integer('End Hour')
    notes = fields.Text('Notes')
