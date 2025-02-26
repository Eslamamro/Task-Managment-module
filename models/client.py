from odoo import models, fields, api

# Client information and all relations are included
class Client(models.Model):
    _name = 'client.info'  

    name = fields.Char(size=50, required=False)
    phone_number = fields.Char(size=11)  # Changed to Char
    address = fields.Char()
    tax_id = fields.Char()  # Changed to Char
    e_invoicing = fields.Boolean()
    username = fields.Char(size=50)
    email = fields.Char()
    password_1 = fields.Char()  # Masking the password
    password_2 = fields.Char()

    income_id = fields.One2many('income', 'client_id' )  
    vat_id = fields.One2many('vat', 'client_id')  
    salary_id = fields.One2many('salary', 'client_id')  
    stamp_id = fields.One2many('stamp', 'client_id')  
    real_state_id = fields.One2many('real_state', 'client_id')  
    withdrawal_id = fields.One2many('withdrawal', 'client_id')
    client_additions_id = fields.One2many('client.additions.wizard', 'client_id')  
    task_id = fields.One2many('task', 'client_id')
    is_income = fields.Boolean(related='client_additions_id.is_income')

    def open_client_additions_wizard(self):
        self.ensure_one()  # Ensures the function is only executed on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Client Additions Wizard',  # Optional: Gives the window a title
            'res_model': 'client.additions.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_client_id': self.id}  # Passes the selected client ID
        }


    
# Wizard to add or remove client taxes
class ClientAdditionsWizard(models.TransientModel):
    _name = 'client.additions.wizard'

    
    is_income = fields.Boolean(string='Income', default=False)
    is_vat = fields.Boolean(string='VAT', default=False)
    is_salary = fields.Boolean(string='Salary', default=False)
    is_stamp = fields.Boolean(string='Stamp', default=False)
    is_real_state = fields.Boolean(string='Real State', default=False)
    is_withdrawal = fields.Boolean(string='Withdrawal', default=False)
    client_id = fields.Many2one('client.info', string="Client", required=True)

 


