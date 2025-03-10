# -*- coding: utf-8 -*-
{
    'name': "Tax Management",

    'summary': "This Module helps you to Manage your clients taxes.",

    'description': """
        Our Tax Management Module is a powerful and user-friendly solution designed to streamline tax-related processes by efficiently managing client data and tracking crucial tax deadlines.
        Built for businesses, accountants, and tax consultants, this module ensures compliance, enhances productivity,
          and minimizes the risk of missed deadlines.
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tax',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security_perms.xml',
        'security/ir.model.access.csv',
        'views/client_info_form.xml',
        'views/client_info_list.xml',
        'views/client_info_kanban.xml',
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

