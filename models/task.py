from odoo import models, fields, api


class Task(models.Model):
    _name = 'task'

    # table fields
    client_id = fields.Many2one('client.info', ondelete='cascade')
    date = fields.Date(string='Created on', default=lambda self: fields.Date.today())
    description = fields.Text(string='Description')
    note = fields.Html(string='Notes')
    tags_ids = fields.Many2many('task.tag', string='Tags')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'pending'),
        ('done', 'Done'),
    ], string='Status', default='pending', track_visibility='onchange', required=True)

    # All Client Tax Categories
    income_id = fields.One2many('income', 'task_id', store=True)
    vat_id = fields.One2many('vat', 'task_id', store=True)  
    salary_id = fields.One2many('salary', 'task_id', store=True)  
    stamp_id = fields.One2many('stamp', 'task_id', store=True)  
    real_state_id = fields.One2many('real_state', 'task_id', store=True)  
    withdrawal_id = fields.One2many('withdrawal', 'task_id', store=True)

    # Visibility fields (linked to client)
    is_income = fields.Boolean(string='Income', related='client_id.is_income', store=True)
    is_vat = fields.Boolean(string='VAT', related='client_id.is_vat', store=True)
    is_salary = fields.Boolean(string='Salary', related='client_id.is_salary', store=True)
    is_stamp = fields.Boolean(string='Stamp', related='client_id.is_stamp', store=True)
    is_real_state = fields.Boolean(string='Real State', related='client_id.is_real_state', store=True)
    is_withdrawal = fields.Boolean(string='Withdrawal', related='client_id.is_withdrawal', store=True)
    

    