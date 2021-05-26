# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        """Override method for sequence assigning"""
        taxes = self.env['account.tax'].search([('code_base', '=', '413')])
        tax = [t.id for t in taxes][0]
        for inv in self:
            for line in inv.invoice_line_ids:
                if not line.invoice_line_tax_ids:
                    tx = [(6, 0, (tax,))]
                    line.write({'invoice_line_tax_ids': tx})

        return super(AccountInvoice, self).invoice_validate()

