# -*- coding: utf-8 -*-
#  Register payment for multiple partners
#  @autor: Marcelo Mora <marcelo.mora@accioma.com>
{
    'name': "Multipartner Register Payment",

    'summary': """
        Register payment for many distinct partners""",

    'author': "Marcelo Mora <marcelo.mora@accioma.com",
    'website': "http://accioma.com",

    'category': 'Accounting',
    'version': '12.0.0.1',

    'depends': ['account'],

    'data': [
        'views/account_payment_view.xml',
    ],
}
