from odoo import models, fields, api

# Client information and all relations are included
class Client(models.Model):
    _name = 'client.info'  

    # Client Information
    name = fields.Char(size=50, required=False, string='Name')
    phone_number = fields.Char(size=11, string='Phone Number')
    address = fields.Char(string='Address')
    tax_number = fields.Char(string='Tax ID')
    e_invoicing = fields.Boolean(string="E-Invoicing", default=False)
    username = fields.Char(size=50, string='Username')
    email = fields.Char(string='Email')
    password_1 = fields.Char(string='Password 1')
    password_2 = fields.Char(string='Password 2')
    registration_number = fields.Char(string="Registration Number")
    date = fields.Date(string="Date")
    registration_company = fields.Char(string="Registration Company")
    token_pass = fields.Char(string="Token Pass")
    portal_request = fields.Selection(
        [
            ('active', 'Active'),
            ('not-active', 'Not-Active'),
            ('unknown_password', 'Unknown_Password'),
            ('waiting', 'Waiting'),
        ],
        string="Portal Request",
        required=False,
        default='not-active'
    )

    # All Client Tax Categories
    income_id = fields.One2many('income', 'client_id')  
    vat_id = fields.One2many('vat', 'client_id')  
    salary_id = fields.One2many('salary', 'client_id')  
    stamp_id = fields.One2many('stamp', 'client_id')  
    real_state_id = fields.One2many('real_state', 'client_id')  
    withdrawal_id = fields.One2many('withdrawal', 'client_id')

    # Wizard state fields (stored directly in client.info)
    is_income = fields.Boolean(string='Income', default=False)
    is_vat = fields.Boolean(string='VAT', default=False)
    is_salary = fields.Boolean(string='Salary', default=False)
    is_stamp = fields.Boolean(string='Stamp', default=False)
    is_real_state = fields.Boolean(string='Real State', default=False)
    is_withdrawal = fields.Boolean(string='Withdrawal', default=False)

    def open_client_additions_wizard(self):
        """Open the wizard to update tax categories visibility"""
        self.ensure_one()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Client Additions Wizard',
            'res_model': 'client.additions.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_client_id': self.id,
                'default_is_income': self.is_income,
                'default_is_vat': self.is_vat,
                'default_is_salary': self.is_salary,
                'default_is_stamp': self.is_stamp,
                'default_is_real_state': self.is_real_state,
                'default_is_withdrawal': self.is_withdrawal,
            },
        }
    
    
# Wizard to add or remove client taxes
class ClientAdditionsWizard(models.TransientModel):
    _name = 'client.additions.wizard'

    client_id = fields.Many2one('client.info', string="Client", required=True)
    is_income = fields.Boolean(string='Income', default=False)
    is_vat = fields.Boolean(string='VAT', default=False)
    is_salary = fields.Boolean(string='Salary', default=False)
    is_stamp = fields.Boolean(string='Stamp', default=False)
    is_real_state = fields.Boolean(string='Real State', default=False)
    is_withdrawal = fields.Boolean(string='Withdrawal', default=False)

    def save_action(self):
        """Save wizard selections to client.info and close"""
        self.ensure_one()
        
        # Update the client's fields with the wizard's selections
        self.client_id.write({
            'is_income': self.is_income,
            'is_vat': self.is_vat,
            'is_salary': self.is_salary,
            'is_stamp': self.is_stamp,
            'is_real_state': self.is_real_state,
            'is_withdrawal': self.is_withdrawal,
        })
        
        return {'type': 'ir.actions.act_window_close'}
 


