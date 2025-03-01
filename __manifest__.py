# -*- coding: utf-8 -*-
{
    'name': "Tax Management",

    'summary': "This Module helps you to Manage your clients taxes.",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security_perms.xml',
        'security/ir.model.access.csv',
        'views/client_info.xml',
        'views/templates.xml',
        'views/menu_items.xml',
        'views/wizards.xml',
        'views/task.xml',
        'views/taxes.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

