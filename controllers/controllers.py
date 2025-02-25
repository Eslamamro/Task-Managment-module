# -*- coding: utf-8 -*-
# from odoo import http


# class TaxManagement(http.Controller):
#     @http.route('/tax__management/tax__management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax__management/tax__management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax__management.listing', {
#             'root': '/tax__management/tax__management',
#             'objects': http.request.env['tax__management.tax__management'].search([]),
#         })

#     @http.route('/tax__management/tax__management/objects/<model("tax__management.tax__management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax__management.object', {
#             'object': obj
#         })

