# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wo_stock_pos = fields.Boolean("POS Sell W/o Stock")

