# -*- coding: utf-8 -*-
{
    'name': "Gestion PTA",

    'sequence': 2,

    'description': """
        Gestion du PTA du MEFPAI
    """,

    'author': "NDEYE SENE de MEFPAI",
    'website': "http://www.odepo.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website','web_timeline'],

    # always loaded
    'data': [
            'templates/portal_login_page.xml',
            'templates/prograpport.xml',
            'views/programme.xml',
            'views/activite.xml',
            'views/service.xml',
            'views/utilisateur.xml',  
            'views/sourcefinancement.xml',
            'security/security.xml',
            'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'auto_install': False,
    'application':True,
}