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

    'version': '0.68',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/cron.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/menu_sections.xml',
        'views/backup.xml',
        'views/branch.xml',
        'views/cloud.xml',
        'views/code.xml',
        'views/code_module.xml',
        'views/code_repository.xml',
        'views/config.xml',
        'views/execution.xml',
        'views/feature.xml',
        'views/float_ip.xml',
        'views/image.xml',
        'views/install.xml',
        'views/key.xml',
        'views/module.xml',
        'views/node.xml',
        'views/node_stat.xml',
        'views/program.xml',
        'views/region.xml',
        'views/domain.xml',
        'views/record.xml',
        'views/repo.xml',
        'views/repo_group.xml',
        'views/restore.xml',
        'views/schedule.xml',
        'views/size.xml',
        'views/volume.xml',
        'wizards/install_wizard.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'data/demo.xml',
    ],
}
