# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store information about Odoo installations requested by clients
# Each installation can have one or more servers (production server, test servers etc)
class Install(models.Model):
    _name = 'unison.install'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True, index=True)
    distro_id = fields.Many2one('unison.distro', 'Distro', ondelete='restrict')
    partner_id = fields.Many2one('res.partner', 'Client', ondelete='restrict')
    domain_name = fields.Char('Domain Name', required=True, index=True)
    manage_dns = fields.Boolean('Manage DNS', default=True)
    volume_gb = fields.Integer('Volume Desired GB', required=True)
    use_floating_ip = fields.Boolean('Use Floating IP', default=False)
    max_servers = fields.Integer('Max Servers', default=1)
    admin_pwd = fields.Char('Admin Password')
    mail_subaccount = fields.Char('Mail Subaccount')
    mail_api_key = fields.Char('Mail API Key')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
