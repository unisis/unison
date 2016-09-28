# -*- coding: utf-8 -*-

from openerp import models, fields

# We provide support for "intermitent" use of installations (just certain hours of the day)
# This model is used to schedule which hours the node should be running each week day.
# Also, it indicates with which node size the installation should be executed: some hours
# of the day could require a more powerful server. This is far simpler than use a cluster
# and their benefits are the same. Using volumes, it's possible switch to a new node size
# in less than 2 minutes.
class Schedule(models.Model):
    _name = 'unison.schedule'
    _rec_name = 'week_day'
    _order = 'week_day'

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    week_day = fields.Integer('Week Day')
    start_hour = fields.Integer('Start Hour')
    end_hour = fields.Integer('End Hour')
    size_id = fields.Many2one('unison.size', 'Size', ondelete='restrict')
    notes = fields.Text('Notes')
