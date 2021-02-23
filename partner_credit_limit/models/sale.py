# See LICENSE file for full copyright and licensing details.


import logging
from odoo import api, models, _
from odoo.exceptions import UserError

_L = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def check_limit(self):
        self.ensure_one()
        partner = self.partner_id
        user_id = self.env['res.users'].search([
            ('partner_id', '=', partner.id)], limit=1)
        if user_id and not user_id.has_group('base.group_portal') or not \
                user_id:
            confirm_sale_order = self.search([('partner_id', '=', partner.id),
                                              ('state', '=', 'sale'),
                                              ('invoice_status', '=', 'to invoice')])
            debit, credit = partner.debit, partner.credit
            amount_total = 0.0
            for status in confirm_sale_order:
                amount_total += status.amount_total
            partner_credit_limit = (partner.credit_limit - credit) + debit
            available_credit_limit = \
                ((partner_credit_limit -
                  (amount_total - debit)) + self.amount_total)

            if (amount_total - debit) > partner_credit_limit:
                if not partner.over_credit:
                    msg = 'Your available credit limit' \
                          ' Amount = %s \nCheck "%s" Accounts or Credit ' \
                          'Limits.' % (available_credit_limit,
                                       self.partner_id.name)
                    raise UserError(_('You can not confirm Sale '
                                      'Order. \n' + msg))
                #  partner.write(
                #      {'credit_limit': credit - debit + self.amount_total})
            return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.env.user.has_group('partner_credit_limit.credit_limit_manager'):
            return res

        for order in self:
            order.check_limit()
        return res

    #  @api.constrains('amount_total'{})
    #  def check_amount(self):
    #      for order in self:
    #          order.check_limit()
