# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions

# This wizard model (TransientModel) is used to configure a new installation
class InstallWizard(models.TransientModel):
    _name = 'unison.install_wizard'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True, index=True)
    size_id = fields.Many2one('unison.size', 'Size', ondelete='restrict')
    site_url = fields.Char('Site URL', required=True, index=True)
    manage_dns = fields.Boolean('Manage DNS', default=True)
    ssl_enabled = fields.Boolean('Enable HTTPS via a SSL certificate', default=True)
    ssl_generate = fields.Boolean('Generate SSL certificate self-signed', default=True)
    ssl_private_key = fields.Text('SSL Private Key')
    ssl_certificate = fields.Text('SSL Certificate')
    ssl_expire_date = fields.Date('SSL Expire Date')
    authorized_ips = fields.Text('Authorized IPs')
    notes = fields.Text('Notes')
    state = fields.Selection([('page1', 'Page 1'),('page2', 'Page 2')])

    @api.multi
    def action_next(self):
        # Apply extra validations to page 1
        if (not self.ssl_enabled and self.ssl_generate):
            raise exceptions.ValidationError('You have requested the generation of a SSL cert, but SSL support is not enabled!')
            return False

        # Update state to page2
        self.write(vals={'state': 'page2'})

        # Return view
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    @api.multi
    def action_previous(self):
        # Update state to  step1
        self.write(vals={'state': 'page1'})

        # Return view
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }

#    @api.multi
#    def do_reopen_form(self):
#        # For details about this function, see 'Odoo Development Essentials' page 115
#        self.ensure_one()
#        return {
#           'type': 'ir.actions.act_window',
#           'res_model': self._name, # this model
#           'res_id': self.id, # the current wizard record
#           'view_type': 'form',
#           'view_mode': 'form',
#           'target': 'new'
#        }
