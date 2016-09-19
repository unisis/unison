# -*- coding: utf-8 -*-

from openerp import models, fields

class Module(models.Model):
     _name = 'unison.module'
     _order = 'name'

     code = fields.Char('Code') # DigitalOcean code, assigned after create
     name = fields.Char('Name', required=True, index=True)
     branch_id = fields.Many2one('unison.branch', 'Branch', ondelete='restrict')
     description = fields.Text('Description')
     summary = fields.Text('Summary')
     category = fields.Char('Category')
     version = fields.Char('Version')
     license = fields.Char('License')
     installable = fields.Boolean('Installable')
     auto_install = fields.Boolean('Auto Install')
     application = fields.Boolean('Application')
     author = fields.Char('Author')
     website = fields.Char('Website')
     db_config = fields.Text('DB Config')
     notes = fields.Text('Notes')
     active = fields.Boolean('Active', default=True)

