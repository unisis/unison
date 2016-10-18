# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This model is used to store information about SSL certificates
# Name is the url of the certificate like unisis.com.ar or www.edif.com.ar
class Certificate(models.Model):
    _name = 'unison.certificate'
    _order = 'name'

    name = fields.Char('Name', required=True, index=True)
    wildcard = fields.Boolean('Wildcard')
    partner_id = fields.Many2one('res.partner', 'Client', ondelete='restrict')
    issued_by = fields.Char('Issued By')
    private_key = fields.Text('Private Key')
    request = fields.Text('Cert Request (CSR)')
    intermediate = fields.Text('Intermediate Cert')
    certificate = fields.Text('Certificate')
    date_issued = fields.Datetime('Date Issued')
    date_expire = fields.Datetime('Date Expire')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
