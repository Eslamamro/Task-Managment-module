from odoo import models, fields, api
# from ..utils import schedule_activitie
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Income(models.Model):
    _name = 'income'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    
    date = fields.Date(string='Date')
    note = fields.Html(string='Note')


    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'income_id')  
    task_id = fields.Many2one('task', ondelete='cascade', unique=True)


    def _schedule_activity(self, tax_category):
        """
        Schedules an activity when the state is set to 'confirm'.
        """ 
        if tax_category == 'income':
            current_year = datetime.now().year
            target_date = datetime(current_year, 12, 15)
        elif tax_category == 'vat':
            current_year = datetime.now().year
            current_month = datetime.now().month
            target_date = datetime(current_year, current_month, 20)
        elif tax_category == 'salary':
            if self.duration == 'monthly':
                current_year = datetime.now().year
                current_month = datetime.now().month
                target_date = datetime(current_year, current_month, 20)
            elif self.duration == 'quarter':
                quarterly_months = [3, 6, 9, 12]  # March, June, September, December
                current_year = datetime.now().year
                for month in quarterly_months:
                    target_date = datetime(current_year, month, 20)
            elif self.duration == 'yearly':
                current_year = datetime.now().year
                target_date = datetime(current_year, 12, 15)
        elif tax_category == 'stamp':
            current_year = datetime.now().year
            target_date = datetime(current_year, 12, 15)
        elif tax_category == 'real_state':
            current_year = datetime.now().year
            target_date = datetime(current_year, 12, 15)
        elif tax_category == 'withdrawal':
            if self.duration == 'jan-mar':
                current_year = datetime.now().year
                target_date = datetime(current_year, 3, 20)
            elif self.quarter_duration == 'apr-jun':
                current_year = datetime.now().year
                target_date = datetime(current_year, 6, 20)
            elif self.quarter_duration == 'jul-sep':
                current_year = datetime.now().year
                target_date = datetime(current_year, 9, 20)
            elif self.quarter_duration == 'oct-dec':
                current_year = datetime.now().year
                target_date = datetime(current_year, 12, 20)
            else:
                quarterly_months = [3, 6, 9, 12]  # March, June, September, December
                current_year = datetime.now().year
                for month in quarterly_months:
                    target_date = datetime(current_year, month, 20)


        activity_type = self.env.ref('mail.mail_activity_data_todo')  # Default To-Do activity
        for record in self:
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get_id(self._name),  # Model ID
                'res_model': self._name,  # Model name as string
                'res_id': record.id,  # Attach to the record
                'activity_type_id': activity_type.id,  # Activity type (To-Do)
                'summary': 'Follow-up Reminder',  # Short description
                'note': 'This is an automated activity.',  # Activity details
                'date_deadline': target_date,  # Deadline
                'user_id': self.env.user.id,  # Assign to the current user
            })
            
    @api.model
    def create(self, vals):
        # Create the record
        record = super(Income, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='income')

        return record
    
    def write(self, vals):
        # Create the record
        result = super(Income, self).create(vals)
        # Schedule an activity
        self._schedule_activity(tax_category='income')
        return result
        



class Vat(models.Model):
    _name = 'vat'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    tax_category = 'vat'

    client_id = fields.Many2one('client.info')  
    documents_id = fields.One2many('documents', 'vat_id')


class Salary(models.Model):
    _name = 'salary'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    tax_category = 'salary'

    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'salary_id')


class Stamp(models.Model):
    _name = 'stamp'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    tax_category = 'stamp'

    client_id = fields.Many2one('client.info')  
    documents_id = fields.One2many('documents', 'stamp_id')


class RealState(models.Model):
    _name = 'real_state'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    tax_category = 'real_state'

    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'real_state_id')  


class Withdrawal(models.Model):
    _name = 'withdrawal'

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    tax_category = 'withdrawal'    

    client_id = fields.Many2one('client.info')
    documents_id = fields.One2many('documents', 'withdrawal_id')  




