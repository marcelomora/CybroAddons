# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import math
from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class AccountVoucher(models.Model):
    _name    = "account.voucher"
    _description = 'Accounting Voucher'
    _inherit = ['account.voucher','mail.thread', 'mail.activity.mixin', 'portal.mixin']

    @api.model
    def _default_journal(self):
        voucher_type = self._context.get('voucher_type', 'sale')
        company_id = self._context.get('company_id', self.env.user.company_id.id)
        domain = [
            ('type', 'in', ('cash','bank')),
            ('company_id', '=', company_id),
        ]
        return self.env['account.journal'].search(domain, limit=1)
    
    journal_id = fields.Many2one('account.journal', 'Journal',
        required=True, readonly=True, states={'draft': [('readonly', False)]}, default=_default_journal)
    number = fields.Char(readonly=False, copy=False)
    account_id = fields.Many2one('account.account', 'Account', required=True, readonly=True, states={'draft': [('readonly', False)]},  domain="[('deprecated', '=', False)]")
    #voucher_type = fields.Selection([('sale', 'Receipt'), ('purchase', 'Payment')], string='Type', required=True, readonly=True, states={'draft': [('readonly', False)]}, oldname="type", default='sale')
    voucher_type = fields.Selection([
        ('sale', 'Receive'),
        ('purchase', 'Payment'),
        ], string='Type', default='purchase', readonly=True, states={'draft': [('readonly', False)]}, oldname="type")
    transaction_type = fields.Selection([('expedition', 'Expedition'), ('regular', 'Regular'),('disposal','Asset Disposal')], string='Transaction Type', readonly=True, states={'draft': [('readonly', False)]})
    
    @api.onchange('partner_id', 'pay_now', 'journal_id')
    def onchange_partner_id(self):
        #print "==onchange_partner_id==",self.pay_now,self.voucher_type
        if self.pay_now == 'pay_now':
            if self.journal_id.type in ('sale','purchase'):
                liq_journal = self.env['account.journal'].search([('type','not in',['sale','purchase'])], limit=1)
                self.account_id = liq_journal.default_debit_account_id \
                    if self.voucher_type == 'sale' else liq_journal.default_credit_account_id
            else:
                self.account_id = self.journal_id.default_debit_account_id \
                    if self.voucher_type == 'sale' else self.journal_id.default_credit_account_id
        else:
            if self.partner_id:
                self.account_id = self.partner_id.property_account_receivable_id \
                    if self.voucher_type == 'sale' else self.partner_id.property_account_payable_id
            elif self.journal_id.type not in ('sale','purchase'):
                self.account_id = False
            else:
                self.account_id = self.journal_id.default_debit_account_id \
                    if self.voucher_type == 'sale' else self.journal_id.default_credit_account_id
    
    @api.multi
    def voucher_move_line_create(self, line_total, move_id, company_currency, current_currency):
        '''
        Create one account move line, on the given account move, per voucher line where amount is not 0.0.
        It returns Tuple with tot_line what is total of difference between debit and credit and
        a list of lists with ids to be reconciled with this format (total_deb_cred,list_of_lists).

        :param voucher_id: Voucher id what we are working with
        :param line_total: Amount of the first line, which correspond to the amount we should totally split among all voucher lines.
        :param move_id: Account move wher those lines will be joined.
        :param company_currency: id of currency of the company to which the voucher belong
        :param current_currency: id of currency of the voucher
        :return: Tuple build as (remaining amount not allocated on voucher lines, list of account_move_line created in this method)
        :rtype: tuple(float, list of int)
        '''
        for line in self.line_ids:
            #create one move line per voucher line where amount is not 0.0
            if not line.price_subtotal:
                continue
            line_subtotal = line.price_subtotal
            if self.voucher_type == 'sale':
                line_subtotal = -1 * line.price_subtotal
            # convert the amount set on the voucher line into the currency of the voucher's company
            amount = self._convert(line.price_unit*line.quantity)
            #===================================================================
            # ALLOW DEBIT AND CREDIT BASED ON MINUS OR PLUS
            #===================================================================
            if (self.voucher_type == 'sale' and amount > 0.0) or (self.voucher_type == 'purchase' and amount < 0.0):
                debit = 0.0
                credit = abs(amount)
            elif (self.voucher_type == 'sale' and amount < 0.0) or (self.voucher_type == 'purchase' or amount > 0.0):
                debit = abs(amount)
                credit = 0.0
            #===================================================================            
            move_line = {
                'journal_id': self.journal_id.id,
                'name': line.name or '/',
                'account_id': line.account_id.id,
                'move_id': move_id,
                'quantity': line.quantity,
                'product_id': line.product_id.id,
                'partner_id': self.partner_id.commercial_partner_id.id,
                'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                #===================================================================     
                'credit': abs(amount) if credit > 0.0 else 0.0,
                'debit': abs(amount) if debit > 0.0 else 0.0,
                #===================================================================
                'date': self.account_date,
                'tax_ids': [(4,t.id) for t in line.tax_ids],
                'amount_currency': line_subtotal if current_currency != company_currency else 0.0,
                'currency_id': company_currency != current_currency and current_currency or False,
                'payment_id': self._context.get('payment_id'),
            }
            # Create one line per tax and fix debit-credit for the move line if there are tax included
            if (line.tax_ids):
                tax_group = line.tax_ids.compute_all(line.price_unit, line.currency_id, line.quantity, line.product_id, self.partner_id)
                if move_line['debit']: move_line['debit'] = tax_group['total_excluded']
                if move_line['credit']: move_line['credit'] = tax_group['total_excluded']
                for tax_vals in tax_group['taxes']:
                    if tax_vals['amount']:
                        tax = self.env['account.tax'].browse([tax_vals['id']])
                        account_id = (amount > 0 and tax_vals['account_id'] or tax_vals['refund_account_id'])
                        if not account_id: account_id = line.account_id.id
                        temp = {
                            'account_id': account_id,
                            'name': line.name + ' ' + tax_vals['name'],
                            'tax_line_id': tax_vals['id'],
                            'move_id': move_id,
                            'date': self.account_date,
                            'partner_id': self.partner_id.id,
                            'debit': self.voucher_type != 'sale' and tax_vals['amount'] or 0.0,
                            'credit': self.voucher_type == 'sale' and tax_vals['amount'] or 0.0,
                            'analytic_account_id': line.account_analytic_id and line.account_analytic_id.id or False,
                        }
                        if company_currency != current_currency:
                            ctx = {}
                            if self.account_date:
                                ctx['date'] = self.account_date
                            temp['currency_id'] = current_currency.id
                            temp['amount_currency'] = company_currency._convert(tax_vals['amount'], current_currency, line.company_id, self.account_date or fields.Date.today(), round=True)
                        self.env['account.move.line'].create(temp)

            self.env['account.move.line'].create(move_line)
        return line_total