# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import hashlib


class res_users(models.Model):
    _inherit = "res.users"

    password_hash = fields.Char('Name', size=128, required=False,)

    @api.model
    def create(self, vals):
        # for record in self:
        if not vals.get('email') and not vals.get('partner_id'):
            vals['email'] = vals.get('login')
        return super(res_users, self).create(vals)

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on
        store fields. Access rights are disabled by
        default, but allowed on some specific fields defined in
        self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(res_users, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.append('password_hash')
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.append('password_hash')
        return init_res

    def _set_password(self, password):
        """ Encrypts then stores the provided plaintext password for the user
        ``id``
        """
        self.password_hash = hashlib.sha1(password.encode()).hexdigest()
        return super(res_users, self)._set_password(password)
