# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    prescriptor_id = fields.Many2one(
        'res.partner',
        'Prescriptor')

