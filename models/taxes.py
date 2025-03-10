from odoo import models, fields, api
# from ..utils import schedule_activitie
from datetime import datetime, date


class Income(models.Model):
    _name = 'income'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    color = fields.Integer("Color")

    
    summary = fields.Many2many('task.tag', string='Summary')  
    client_id = fields.Many2one('client.info', string='Client Name')
    task_id = fields.Many2one('task')


    
    def _schedule_activity(self, tax_category):
        """Scheduling automated activities depending on the type of tax """
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
            'summary': self.summary,
            'note': 'This is an automated activity.',
            'date_deadline': deadline_date,  # Corrected: Now uses a specific datetime
            'user_id': self.env.user.id,
        })

    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()

    @api.model
    def create(self, vals):
        """Ensures that the task gets created with its related activity"""
        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

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
    summary = fields.Many2many('task.tag', string='Summary')
    client_id = fields.Many2one('client.info')  
    task_id = fields.Many2one('task')

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


    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()

    @api.model
    def create(self, vals):

        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

        # Create the record
        record = super(Vat, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='vat')

        return record


class Salary(models.Model):
    _name = 'salary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    summary = fields.Many2many('task.tag', string='Summary')
    date = fields.Date(string='Date')
    note = fields.Html(string='Note')
    duration = fields.Selection(
        [
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('quarter', 'Quarter'),

        ],
        string='Duration',
        default=False
    ) 

    client_id = fields.Many2one('client.info')
    task_id = fields.Many2one('task')

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
                'quarter': [(current_year, month, 15) for month in [3, 6, 9, 12]]
            }.get(self.duration, None),  # Return None if duration is None
            'withdrawal': {
            'jan-mar': (current_year, 3, 15),
            'apr-jun': (current_year, 6, 15),
            'jul-sep': (current_year, 9, 15),
            'oct-dec': (current_year, 12, 15),
            }.get(self.duration, [(current_year, month, 15) for month in [3, 6, 9, 12]]),  # If None, set for all quarters
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


    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()

    @api.model
    def create(self, vals):

        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

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
    summary = fields.Many2many('task.tag', string='Summary')
    client_id = fields.Many2one('client.info')  
    task_id = fields.Many2one('task')
    
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

    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()

    @api.model
    def create(self, vals):

        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

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
    summary = fields.Many2many('task.tag', string='Summary')
    client_id = fields.Many2one('client.info')    
    task_id = fields.Many2one('task')

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

    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()

    @api.model
    def create(self, vals):

        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

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
    summary = fields.Many2many('task.tag', string='Summary')
    duration = fields.Selection(
            [
                ('jan-mar', 'January - March'),
                ('apr-jun', 'April - June'),
                ('jul-sep', 'July - September'),
                ('oct-dec', 'October - December'),
            ],
            string='Duration',
            default=None
        )
    client_id = fields.Many2one('client.info')    
    task_id = fields.Many2one('task')

    def _schedule_activity(self, tax_category):
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Dictionary-based logic for tax deadlines, including salary & withdrawal
        tax_deadlines = {
            'income': (current_year, 12, 15),
            'stamp': (current_year, 12, 15),
            'real_state': (current_year, 12, 15),
            'vat': (current_year, current_month, 15),
            'salary': {
                'monthly': (current_year, current_month, 15),
                'yearly': (current_year, 12, 15),
                'quarter': [(current_year, month, 20) for month in [3, 6, 9, 12]]
            }.get(self.duration, None),  # Return None if duration is None
            'withdrawal': {
            'jan-mar': (current_year, 3, 15),
            'apr-jun': (current_year, 6, 15),
            'jul-sep': (current_year, 9, 15),
            'oct-dec': (current_year, 12, 15),
            }.get(self.duration, [(current_year, month, 15) for month in [3, 6, 9, 12]]),  # If None, set for all quarters
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

    def action_done_activity(self):
        """Mark the related activity as Done."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.action_done()

    def action_cancel_activity(self):
        """Cancel the related activity (unlink it)."""
        activities = self.env['mail.activity'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
        ])
        for activity in activities:
            activity.unlink()
            
    @api.model
    def create(self, vals):

        # Fetch or create a task for the client
        client_id = vals.get('client_id')
        if client_id:
            # Search for the latest "pending" task for the SAME client
            pending_task = self.env['task'].search(
                [('client_id', '=', client_id), ('state', '=', 'pending')],
                order="create_date desc",
                limit=1
            )

            # If a pending task exists for this client, use it. Otherwise, create a new one.
            if pending_task:
                task = pending_task
            else:
                task = self.env['task'].create({
                    'client_id': client_id
                })

            vals['task_id'] = task.id  # Assign the income record to the correct task.

        # Create the record
        record = super(Withdrawal, self).create(vals)
        # Schedule an activity
        record._schedule_activity(tax_category='withdrawal')

        return record


class TaskTag(models.Model):
    _name = 'task.tag'
    _description = 'Task Tag'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")

    @api.model
    def _create_default_tags(self):
        """Create default tags with Odoo colors."""
        default_tags = [
            {'name': 'Urgent', 'color': 1},  # Red
            {'name': 'Important', 'color': 2},  # Green
            {'name': 'Low Priority', 'color': 3},  # Blue
            {'name': 'Review', 'color': 4},  # Yellow
        ]

        for tag in default_tags:
            if not self.search([('name', '=', tag['name'])]):
                self.create(tag)

    @api.model
    def init(self):
        """Automatically create default tags when the module is installed."""
        self._create_default_tags()

