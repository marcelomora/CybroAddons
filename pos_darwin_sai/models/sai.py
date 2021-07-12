# -*- encoding: utf-8 -*-
# Copyright 2021 Accioma (https://accioma.com).
# @author marcelomora <java.diablo@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class PharmacySymptom(models.Model):
    _name = 'pharmacy.symptom'
    _description = 'Pharmacy Symptom'

    name = fields.Char()

class PharmacyActivePrinciple(models.Model):
    _name = 'pharmacy.active.principle'
    _description = 'Pharmacy Active Principle'

    name = fields.Char()

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    symptom_ids = fields.Many2many(
        comodel_name='pharmacy.symptom',
        string='Symptom')

    active_principle_id = fields.Many2one(
        'pharmacy.active.principle',
        'Active Principle')

