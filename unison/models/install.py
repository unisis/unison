# -*- coding: utf-8 -*-

from openerp import models, fields

# This model is used to store information about Odoo installations requested by clients
# Each installation has a production installation and a test installation on the same node.
# Each prod/inst installation is composed by a distro version (set of repos and modules
# provided by UniSis) and an optional install version (additional set of custom modules)
class Install(models.Model):
    _name = 'unison.install'
    _order = 'name'

    statuses = [
        ('inserted', 'Inserted'),         # This is the first status, inserted in database, creation not sent to DigitalOcean yet
        ('provisioning', 'Provisioning'), # Creation of node sent to DigitalOcean, waiting their creation
        ('installing', 'Installing'),     # Node was created, we are initializing/setting their containers
        ('starting', 'Starting'),         # Initialization finalized, requested start of services (also used after stop an installation)
        ('started', 'Started'),           # Installation is online and ready to be used
        ('stopping', 'Stopping'),         # UniSon or user has requested the stop of the installation
        ('stopped', 'Stopped'),           # Installation was stopped intentionally
        ('crashed', 'Crashed'),           # Installation should be online/started, but it seems unresponsive/crashed at this moment
        ('deleted', 'Deleted'),           # Installation was deleted from database, termination not sent to DigitalOcean yet
        ('terminating', 'Terminating'),   # Requested termination of node on DigitalOcean
        ('terminated', 'Terminated'),     # Node was termnated as well any other resource related to this installation
    ]

    name = fields.Char('Name', required=True, index=True)
    description = fields.Char('Description', required=True, index=True)
    distro_id = fields.Many2one('unison.distro', 'Distro', ondelete='restrict')
    site_url = fields.Char('Site URL', required=True, index=True)
    partner_id = fields.Many2one('res.partner', 'Client', ondelete='restrict')
    manage_dns = fields.Boolean('Manage DNS', default=True)
    site_record_id = fields.Many2one('unison.record', 'DNS Record', ondelete='restrict')
    status = fields.Selection(statuses, 'Status', default='inserted')
    admin_pwd = fields.Char('Admin Password')
    prod_distro_version_id = fields.Many2one('unison.version', 'Prod Distro Version', required=True, ondelete='restrict')
    prod_install_version_id = fields.Many2one('unison.version', 'Prod Install Version', ondelete='restrict')
    test_distro_version_id = fields.Many2one('unison.version', 'Test Distro Version', required=True, ondelete='restrict')
    test_install_version_id = fields.Many2one('unison.version', 'Test Install Version', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    volume_gb = fields.Integer('Volume Desired GB', required=True)
    volume_id = fields.Many2one('unison.volume', 'Volume', ondelete='restrict')
    floating_ip_id = fields.Many2one('unison.floating_ip', 'Floating IP', ondelete='restrict')
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
