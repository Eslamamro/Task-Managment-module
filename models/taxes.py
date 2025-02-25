from odoo import models, fields, api

class Income(models.Model):
    _name = 'income'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')

    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'income_id')  


class Vat(models.Model):
    _name = 'vat'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    
    client_id = fields.Many2one('client.info')  
    documents_id = fields.One2many('documents', 'vat_id')


class Salary(models.Model):
    _name = 'salary'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    
    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'salary_id')


class Stamp(models.Model):
    _name = 'stamp'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    
    client_id = fields.Many2one('client.info')  
    documents_id = fields.One2many('documents', 'stamp_id')


class RealState(models.Model):
    _name = 'real_state'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    
    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'real_state_id')  


class Withdrawal(models.Model):
    _name = 'withdrawal'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    
    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'withdrawal_id')  