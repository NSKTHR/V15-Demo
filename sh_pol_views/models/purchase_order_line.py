# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models, _, tools


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    image = fields.Image(string=" ", compute='_compute_image')
    qty_unreceived = fields.Float(string="Unreceived Quantity", compute='_compute_qty_bill')
    qty_unbilled = fields.Float(string="Unbilled Quantity", compute='_compute_qty_bill')
    bills_remaining = fields.Float(string="Forecasted Bills", compute='_compute_qty_bill')
    categ_id = fields.Many2one('product.category', string="Product Category")
    
    qty_unreceived_filter = fields.Float(string="Unreceived Qty")
    qty_unbilled_filter = fields.Float(string="Unbilled Qty")
    bills_remaining_filter = fields.Float(string="Forecasted Bill")
    
    @api.depends('qty_received','qty_invoiced','product_qty','product_id','categ_id')
    def _compute_qty_bill(self):
        """Compute the unreceived qty,unbilled qty and remaining bills forcasted"""
        for record in self:
            if record.product_qty:
                record.qty_unreceived = record.product_qty - record.qty_received
                record.qty_unbilled = record.qty_received - record.qty_invoiced
                record.bills_remaining = record.product_qty - record.qty_invoiced
                
                record.qty_unreceived_filter = record.qty_unreceived
                record.qty_unbilled_filter = record.qty_unbilled
                record.bills_remaining_filter = record.bills_remaining
                record.categ_id = record.product_id.categ_id
                
            else:
                record.qty_unreceived=0
                record.qty_unbilled=0
                record.bills_remaining=0
                
                record.qty_unreceived_filter = record.qty_unreceived
                record.qty_unbilled_filter = record.qty_unbilled
                record.bills_remaining_filter = record.bills_remaining
                record.categ_id = record.product_id.categ_id
                
            

    def _compute_image(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image = record.product_id.image_variant_1920 or record.product_id.product_tmpl_id.image_1920
