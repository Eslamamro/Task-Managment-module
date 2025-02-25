from odoo import models, fields, api

class Documents(models.Model):
    _name = 'documents'

    name = fields.Char(string='Name')
    upload = fields.Binary(string='Upload', attachment=True)
     
    income_id = fields.Many2one('income')  
    vat_id = fields.Many2one('vat')  
    salary_id = fields.Many2one('salary')  
    stamp_id = fields.Many2one('stamp')  
    real_state_id = fields.Many2one('real_state')  
    withdrawal_id = fields.Many2one('withdrawal')  
