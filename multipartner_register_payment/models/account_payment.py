# coding: utf-8
"""Account Register Payment inheritance"""

import logging
from odoo import models, fields, api

MAP_INVOICE_TYPE_PAYMENT_SIGN = {
    'out_invoice': 1,
    'in_refund': -1,
    'in_invoice': -1,
    'out_refund': 1,
}

_L = logging.getLogger(__name__)


class AccountRegisterPayments(models.TransientModel):
    """Account Register Payments inheritance"""
    _inherit = 'account.register.payments'
    _description = 'Account Register Payments'

    one_payment = fields.Boolean("One Payment")

    @api.multi
    def _groupby_invoices(self):
        '''Groups the invoices linked to the wizard.

        If the one_payment option is activated, invoices will be grouped
        in just one payment. Otherwise,
        invoices will be grouped as selected in base class.

        :return: a dictionary mapping, grouping invoices as a recordset under each of its keys.
        '''

        return {1: self.invoice_ids}

    @api.multi
    def _prepare_payment_vals(self, invoices):
        vals = super(AccountRegisterPayments, self)._prepare_payment_vals(invoices)
        vals['one_payment'] = self.one_payment
        return vals

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    one_payment = fields.Boolean("One Payment")

    def _create_payment_entry(self, amount):
        """ create a journal entry corresponding to a payment, if the payment references invoice(s) they are reconciled.
            return the journal entry.
        """
        if not self.one_payment:
            return super(AccountPayment, self)._create_payment_entry(amount)

        AccountAbstractPayment = self.env["account.abstract.payment"]
        AccountMoveLine = self.env['account.move.line'].with_context(check_move_validity=False)
        move = self.env['account.move'].create(self._get_move_vals())
        invoice_datas = self.invoice_ids.read_group(
            [('id', 'in', self.invoice_ids.ids)],
            ['partner_id', 'currency_id', 'type', 'residual_signed'],
            ['partner_id', 'currency_id', 'type'], lazy=False)

        # Get the payment currency
        currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id or invoices and invoices[0].currency_id

        for invoice_data in invoice_datas:
            total = 0.0
            amount_total = MAP_INVOICE_TYPE_PAYMENT_SIGN[invoice_data['type']] * invoice_data['residual_signed']
            payment_currency = self.env['res.currency'].browse(
                invoice_data['currency_id'][0])
            if payment_currency == currency:
                total = amount_total
            else:
                total = payment_currency._convert(amount_total, currency, self.env.user.company_id, self.payment_date or fields.Date.today())

            if total != 0.0:
                debit, credit, amount_currency, currency_id =\
                    AccountMoveLine.with_context(
                            date=self.payment_date)._compute_amount_fields(
                                total,
                                self.currency_id,
                                self.company_id.currency_id)
                counterpart_aml_dict = self._get_shared_move_line_vals(
                    debit, credit, amount_currency, move.id, False)
                counterpart_aml_dict.update(
                    self._get_counterpart_move_line_vals(self.invoice_ids))
                counterpart_aml_dict.update({'currency_id': currency_id})
                counterpart_aml = aml_obj.create(counterpart_aml_dict)

            #reconcile with the invoices
            if self.payment_difference_handling == 'reconcile' and self.payment_difference:
                writeoff_line = self._get_shared_move_line_vals(0, 0, 0, move.id, False)
                debit_wo, credit_wo, amount_currency_wo, currency_id = AccountMoveLine.with_context(date=self.payment_date)._compute_amount_fields(self.payment_difference, self.currency_id, self.company_id.currency_id)
                writeoff_line['name'] = self.writeoff_label
                writeoff_line['account_id'] = self.writeoff_account_id.id
                writeoff_line['debit'] = debit_wo
                writeoff_line['credit'] = credit_wo
                writeoff_line['amount_currency'] = amount_currency_wo
                writeoff_line['currency_id'] = currency_id
                writeoff_line = aml_obj.create(writeoff_line)
                if counterpart_aml['debit'] or (writeoff_line['credit'] and not counterpart_aml['credit']):
                    counterpart_aml['debit'] += credit_wo - debit_wo
                if counterpart_aml['credit'] or (writeoff_line['debit'] and not counterpart_aml['debit']):
                    counterpart_aml['credit'] += debit_wo - credit_wo
                counterpart_aml['amount_currency'] -= amount_currency_wo

            #write counterpart lines
            if not self.currency_id.is_zero(self.amount):
                if not self.currency_id != self.company_id.currency_id:
                    amount_currency = 0
                liquidity_aml_dict = self._get_shared_move_line_vals(credit, debit, -amount_currency, move.id, False)
                liquidity_aml_dict.update(self._get_liquidity_move_line_vals(-amount))
                AccountMoveLine.create(liquidity_aml_dict)

            #reconcile the invoice receivable/payable line(s) with the payment
            if self.invoice_ids:
                self.invoice_ids.register_payment(counterpart_aml) #Error FIXME

        #validate the payment
        if not self.journal_id.post_at_bank_rec:
            move.post()

        return move
