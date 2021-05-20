# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'

    prescriptor_id = fields.Many2one(
        'res.partner',
        'Prescriptor')

    @api.model
    def invoice_paid(self, limit=1):
        orders = self.search([('state', '=', 'paid')], order="date_order", limit=limit)

        for o in orders:
            o.action_pos_order_invoice()
            #  _logger.info("Orden facturada {}".format(o.id))

