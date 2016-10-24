# -*- coding: utf-8 -*-

from openerp import models, fields, api

# This class is used to store general configurations
# not directly related to any other model.
class Config(models.Model):
    _name = 'unison.config'
    _order = 'id'

    port_nginx = fields.Integer('NginX Port')
    port_odoo = fields.Integer('Odoo Port')
    port_pgsql = fields.Integer('PgSQL Port')
    port_aeroo = fields.Integer('Aeroo Port')
    s3_access_key = fields.Char('S3 Access Key')
    s3_secret_key = fields.Char('S3 Secret Key')
    s3_backups_bucket = fields.Char('S3 Backups Bucket')
    smtp_host_name = fields.Char('SMTP Host Name')
    smtp_port_number = fields.Char('SMTP Port Number')
    smtp_user_name = fields.Char('SMTP User Name')
    smtp_user_pwd = fields.Char('SMTP User Password')
    smtp_sender_address = fields.Char('SMTP Sender Address')
    smtp_alerts_recipient = fields.Char('SMTP Alerts Recipient')
    notes = fields.Text('Notes')
    active = fields.Boolean('Active', default=True)
