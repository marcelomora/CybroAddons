# -*- coding: utf-8 -*-
#
#
#    Copyright (c) 2016 Sucros Clear Information Technologies PLC.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this pr ogram.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    'name': "Accounting Petty Cash reciept",
    'summary': "Automated management of petty cash funds",
    'description': """
    """,
    'author': 'Select Solutions',
    'website': "http://select-online.net",
    'license': "AGPL-3",
    'version': '11.0.1.0',
    'category': 'Accounting',
    'depends': ['base','account','account_voucher','product'],
     'data':[
         'security/petty_cash.xml',
         'security/ir.model.access.csv',
        'wizard/change_fund_view.xml',
        'wizard/close_fund_view.xml',
        'wizard/create_fund_view.xml',
        'wizard/issue_voucher_view.xml',
        'wizard/reconcile_view.xml',
        'wizard/reopen_view.xml',
        'views/petty_cash_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}
