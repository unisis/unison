# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store information about an installation server
# Each server have their own distro version (distro_version_id, 
# set of repos and modules provided by UniSis) and an optional install version 
# (install_version_id, additional set of custom modules created by user)
class Server(models.Model):
    _name = 'unison.server'
    _order = 'install_id, host_name'

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

    install_id = fields.Many2one('unison.install', 'Install', ondelete='restrict')
    is_test = fields.Boolean('Is Test', required=True)
    host_name = fields.Char('Host Name', required=True, index=True, default="www")
    description = fields.Char('Description', required=True, index=True)
    status = fields.Selection(statuses, 'Status', default='inserted')
    distro_version_id = fields.Many2one('unison.version', 'Distro Version', required=True, ondelete='restrict')
    install_version_id = fields.Many2one('unison.version', 'Install Version', ondelete='restrict')
    certificate_id = fields.Many2one('unison.certificate', 'Certificate', ondelete='restrict')
    node_id = fields.Many2one('unison.node', 'Node', ondelete='restrict')
    volume_id = fields.Many2one('unison.volume', 'Volume', ondelete='restrict')
    floating_ip_id = fields.Many2one('unison.floating_ip', 'Floating IP', ondelete='restrict')
    record_id = fields.Many2one('unison.record', 'DNS Record', ondelete='restrict')
    monthly_hours_limit = fields.Integer('Monthly Execution Hours Limit', default=0)
    authorized_ips = fields.Char('Authorized IPs')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)

    # Return as name the hostname and the domain name
    def _get_name(self):
        return self.host_name + "." + self.install_id.domain_name
