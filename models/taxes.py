from odoo import models, fields, api
# from ..utils import schedule_activitie
from datetime import datetime, date


class Income(models.Model):
    _name = 'income'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')

    client_id = fields.Many2one('client.info', string='Client Name')
    task_id = fields.Many2one('task', ondelete='cascade', unique=True)


    def _schedule_activity(self, tax_category):

        # (note)add back the withdrawal and the salary in the dic next update'''

        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(Income, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='income')
        return record
        

class Vat(models.Model):
    _name = 'vat'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')

    client_id = fields.Many2one('client.info')  


    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(Vat, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='vat')

        return record


class Salary(models.Model):
    _name = 'salary'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    duration = fields.Selection(
        [
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('quarter', 'Quarter'),

        ],
        string='Salary Duration',
        default=False
    ) 

    client_id = fields.Many2one('client.info')

    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
            'salary': {
                'monthly': (current_year, current_month, 20),
                'yearly': (current_year, 12, 15),
                'quarter': [(current_year, month, 20) for month in [3, 6, 9, 12]]
            }.get(self.duration, None),  # Return None if duration is None
            'withdrawal': {
            'jan-mar': (current_year, 3, 20),
            'apr-jun': (current_year, 6, 20),
            'jul-sep': (current_year, 9, 20),
            'oct-dec': (current_year, 12, 20),
            }.get(self.duration, [(current_year, month, 20) for month in [3, 6, 9, 12]]),  # If None, set for all quarters
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(Salary, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='salary')

        return record


class Stamp(models.Model):
    _name = 'stamp'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')

    client_id = fields.Many2one('client.info')  

    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(Stamp, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='stamp')

        return record


class RealState(models.Model):
    _name = 'real_state'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')

    client_id = fields.Many2one('client.info')    

    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(RealState, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='real_state')

        return record


class Withdrawal(models.Model):
    _name = 'withdrawal'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    duration = fields.Selection(
            [
                ('jan-mar', 'January - March'),
                ('apr-jun', 'April - June'),
                ('jul-sep', 'July - September'),
                ('oct-dec', 'October - December'),
            ],
            string='Withdrawal Duration',
            default=None
        )
    client_id = fields.Many2one('client.info')    

    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 20),
            'salary': {
                'monthly': (current_year, current_month, 20),
                'yearly': (current_year, 12, 15),
                'quarter': [(current_year, month, 20) for month in [3, 6, 9, 12]]
            }.get(self.duration, None),  # Return None if duration is None
            'withdrawal': {
            'jan-mar': (current_year, 3, 20),
            'apr-jun': (current_year, 6, 20),
            'jul-sep': (current_year, 9, 20),
            'oct-dec': (current_year, 12, 20),
            }.get(self.duration, [(current_year, month, 20) for month in [3, 6, 9, 12]]),  # If None, set for all quarters
        }

        deadline_date = tax_deadlines.get(tax_category)

        if not deadline_date:
            return None  # Exit if no deadline is found

        # Handle multiple dates for quarterly salary tax
        if isinstance(deadline_date, list):
            for date in deadline_date:
                self._create_activity(datetime(*date))
        else:
            self._create_activity(datetime(*deadline_date))

    def _create_activity(self, deadline_date):
        """Helper method to create mail.activity."""
        activity_type = self.env.ref('mail.mail_activity_data_todo')

        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get_id(self._name),
            'res_model': self._name,
            'res_id': self.id,
            'activity_type_id': activity_type.id,
            'summary': 'Follow-up Reminder',
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })


    @api.model
    def create(self, vals):
        # Create the record
        record = super(Withdrawal, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='withdrawal')

        return record
