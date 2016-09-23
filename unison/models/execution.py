# -*- coding: utf-8 -*-

from openerp import models, fields

# We provide support for "intermitent" use of installations (just certain hours of the day)
# This model is used to regiter the different periods of execution for log and billing purposes
# Normally, these cycles are defined by the schedule model and are automatic, but is also possible
# control these periods manually from our dashboard (for example, to stop the installation during a holiday day)
class Execution(models.Model):
    _name = 'unison.execution'
    _rec_name = 'id'
    _order = 'date_start'

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    hours = fields.Integer('Hours')
    started_manually = fields.Boolean('Started Manually')
    stopped_manually = fields.Boolean('Stopped Manually')
    node_price_usd = fields.Float('Node Price USD')
    volume_price_usd = fields.Float('Volume Price USD')
    notes = fields.Text('Notes')
