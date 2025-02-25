from odoo import models, fields, api

class Task(models.Model):
    _name = 'task'

    client_id = fields.Many2one('client.info', string='Name')
    