# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to indicate which modules should be automatically installed
# when a new installation is required
class VersionModule(models.Model):
    _name = 'unison.version_module'
    _rec_name = 'module_name'
    _order = 'module_name'

    version_id = fields.Many2one('unison.version', 'Version', ondelete='restrict')
    module_name = fields.Char('Module', required=True, index=True)
