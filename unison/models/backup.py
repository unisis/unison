# -*- coding: utf-8 -*-

from openerp import models, fields

# This model store the backups created to installations (on their production or test database)
class Backup(models.Model):
     _name = 'unison.backup'
     _order = 'install_id, date_start'

     name = fields.Char('Name', required=True, index=True)
     description = fields.Char('Description')
     install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
     test_db = fields.Boolean('On Test DB?')
     automatic = fields.Boolean('Is Automatic?')
     program_id = fields.Many2one('unison.program', 'Program', ondelete='restrict')
     code_id = fields.Many2one('unison.code', 'Code', ondelete='restrict')
     date_start = fields.Datetime('Date Start')
     date_end = fields.Datetime('Date End')
     db_mb = fields.Integer('Database MB')
     fs_mb = fields.Integer('Files MB')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active?')
