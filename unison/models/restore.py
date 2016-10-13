# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model store the restores performed on installations (on their production or test database)
class Restore(models.Model):
    _name = 'unison.restore'
    _order = 'install_id, date_start'

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    backup_id = fields.Many2one('unison.backup', 'Backup', ondelete='restrict')
    restore_code = fields.Boolean('Restore Code?', default=True)
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    success = fields.Boolean('Success?')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active?')
