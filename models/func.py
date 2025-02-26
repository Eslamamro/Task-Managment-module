from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


def schedule_activitie(self, tax_category):
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
            
        for record in self:
            # change to category variable late and use this code // note = 'VAT Activity' if record.category == 'vat' else 'Salary Activity' 
            # if record.category == 'salary' else 'General Activity'
            note = 'VAT Activity' if tax_category == 'vat' else 'Salary Activity' if tax_category == 'salary' else 'General Activity'
            self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get('task').id,
                'res_id': self.task_id.id,
                'res_name': self.name if self.name else "Unknown Client",
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'summary': 'Follow up for confirmation',
                'note': note,
                'date_deadline': target_date,  # Always set to the 24th of the current month
                'user_id': self.env.user.id,  # Assigned to the current user
            })
