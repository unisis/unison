# -*- coding: utf-8 -*-
{
    'name': "UniSon",

    'application': True,

    # UniSon modules are proprietary software, but Odoo only supports a fixed number of licenses
    'license': "GPL-3",

    'summary': "UniSis Management System",

    'description': "Manages the creation of nodes, installations and their operations (backups, restores, health checks, etc)",

    'author': "UniSis",

    'website': "https://www.unisis.com.ar",

    'category': 'Administration',

    'version': '0.36',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/menu_sections.xml',
        'views/cloud.xml',
        'views/image.xml',
        'views/key.xml',
        'views/node.xml',
        'views/node_stat.xml',
        'views/region.xml',
        'views/domain.xml',
        'views/record.xml',
        'views/repository.xml',
        'views/repository_type.xml',
        'views/size.xml',
        'views/volume.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'data/demo.xml',
    ],
}
