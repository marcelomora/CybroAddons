# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def validate_draft(self):
        invs = self.search([
            ('state', '=', 'draft'),
            ('type', '=', 'out_invoice'),
            ], limit = 200, order = 'id desc')

        for i in invs:
            # _logger.info("Factura {}".format(i.id))
            try:
                i.action_invoice_open()
            except:
                continue

    @api.model
    def compute_amount(self):

        invs = self.search([
            ('type', '=', 'out_invoice'),
            ('state', 'in', ('open', 'paid', ))
            ], order="id asc")

        for i in invs:
            i._onchange_invoice_line_ids()
            i._compute_amount()
            _logger.info("FActura base vat 0 {} {}".format(i.id, i.amount_base_vat_0))

    @api.multi
    def compute_amount_by_id(self):
        self.ensure_one()

        self._onchange_invoice_line_ids()
        self._compute_amount()
        return "Factura base vat 0 {} {}".format(self.id, self.amount_base_vat_0)
