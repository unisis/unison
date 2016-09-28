# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store information about Odoo installations requested by clients
# Each installation has a production installation and a test installation on the same node
class Install(models.Model):
    _name = 'unison.install'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True, index=True)
    site_url = fields.Char('Site URL', required=True, index=True)
    partner_id = fields.Many2one('res.partner', 'Client', ondelete='restrict')
    manage_dns = fields.Boolean('Manage DNS', default=True)
    site_record_id = fields.Many2one('unison.record', 'DNS Record', ondelete='restrict')
    status = fields.Char('Status')
    admin_pwd = fields.Char('Admin Password')
    prod_code_id = fields.Many2one('unison.code', 'Prod Code', ondelete='restrict')
    test_code_id = fields.Many2one('unison.code', 'Test Code', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    volume_id = fields.Many2one('unison.volume', 'Volume', ondelete='restrict')
    float_ip_id = fields.Many2one('unison.float_ip', 'Float IP', ondelete='restrict')
    mail_subaccount = fields.Char('Mail Subaccount')
    mail_api_key = fields.Char('Mail API Key')
    ssl_enabled = fields.Boolean('Enable HTTPS via a SSL certificate', default=True)
    ssl_generate = fields.Boolean('Generate SSL certificate self-signed', default=True)
    ssl_private_key = fields.Text('SSL Private Key')
    ssl_certificate = fields.Text('SSL Certificate')
    ssl_expire_date = fields.Date('SSL Expire Date')
    authorized_ips = fields.Text('Authorized IPs')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
