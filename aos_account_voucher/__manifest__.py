# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Account Voucher',
    'version': '12.0.0.1.0',
    'license': 'AGPL-3',
    'summary': 'Account Voucher Management',
    'sequence': 1,
    "author": "Alphasoft",
    'description': """
Account Voucher
====================
    """,
    'category' : 'Account Voucher Management',
    'website': 'https://www.alphasoft.co.id/',
    'images':  ['images/main_screenshot.png'],
    'depends' : ['account_voucher', 'aos_base_account'],
    'data': [
        'security/account_security.xml',
        'views/account_voucher_view.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    #'post_init_hook': '_auto_install_l10n',
}
