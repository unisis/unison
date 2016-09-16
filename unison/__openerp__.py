# -*- coding: utf-8 -*-
{
    'name': "unison",

    'application': True,

    # UniSon modules are proprietary software, but Odoo only supports a fixed number of licenses
    'license': "GPL-3",

    'summary': "UniSis Management System",

    'description': "Manages the creation of nodes, installations and their operations (backups, restores, health checks, etc)",

    'author': "UniSis",

    'website': "https://www.unisis.com.ar",

    'category': 'Administration',

    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/repository_type.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'data/demo.xml',
    ],
}
