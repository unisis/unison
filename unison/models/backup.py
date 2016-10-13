# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model store the backups created to installations (on their production or test database)
# We just include database backup and data files backup. Regarding the code, we store the
# base version id and -if there are some changed files not saved as a version- we just copy
# these files using rsync (the changed code files) to restore these files later if required
class Backup(models.Model):
    _name = 'unison.backup'
    _order = 'install_id, date_start'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description')
    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    test_db = fields.Boolean('Backup Test DB?')
    automatic = fields.Boolean('Is Automatic?')
    program_id = fields.Many2one('unison.program', 'Program', ondelete='restrict')
    version_id = fields.Many2one('unison.version', 'Code', ondelete='restrict')
    changed_code = fields.Boolean('Has changed code?')
    date_start = fields.Datetime('Date Start')
    date_end = fields.Datetime('Date End')
    db_mb = fields.Integer('Database MB')
    fs_mb = fields.Integer('Files MB')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active?')
