# -*- coding: utf-8 -*-
# Copyright 2019 Linksoft Mitra Informatika
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
# noinspection PyUnresolvedReferences,SpellCheckingInspection
{
    "name": """Show Import Bank Statement Button""",
    "summary": """Show import button in bank/cash statement.""",
    "category": "Extra Tools",
    "version": "12.0.0.1.0",
    "development_status": "Alpha",  # Options: Alpha|Beta|Production/Stable|Mature
    "application": False,
    "images": [
        'images/main_screenshot.png',
        'images/main_1.png'
    ],
    # "price": 10.00,
    # "currency": "EUR",

    "author": "Linksoft Mitra Informatika",
    "support": "support@linksoft.id",
    "website": "https://linksoft.id",
    "license": "OPL-1",

    "depends": [
        # odoo addons
        'base',
        'account',
        # third party addons

        # developed addons
    ],
    "excludes": [
        "ls_account",
    ],
    "data": [
        # group

        # data

        # action
        # 'views/action.xml',

        # view

        # assets
        'views/assets.xml',

        # wizard

        # onboarding

        # action menu
        # 'views/action_menu.xml',

        # action onboarding
        # 'views/action_onboarding.xml',

        # menu
        # 'views/menu.xml'

        # security
        # 'security/ir.model.access.csv',

        # data
    ],
    "demo": [
        # 'demo/demo.xml',
    ],
    "qweb": [
        # "static/src/xml/{QWEBFILE1}.xml",
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,

    "auto_install": False,
    "installable": True,

    "external_dependencies": {"python": [], "bin": []},
    # "live_test_url": "",
    # "demo_title": "{MODULE_NAME}",
    # "demo_addons": [
    # ],
    # "demo_addons_hidden": [
    # ],
    # "demo_url": "DEMO-URL",
    # "demo_summary": "{SHORT_DESCRIPTION_OF_THE_MODULE}",
    # "demo_images": [
    #    "images/MAIN_IMAGE",
    # ]
}
