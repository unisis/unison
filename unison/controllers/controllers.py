# -*- coding: utf-8 -*-
from openerp import http

# class Unison(http.Controller):
#     @http.route('/unison/unison/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unison/unison/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unison.listing', {
#             'root': '/unison/unison',
#             'objects': http.request.env['unison.unison'].search([]),
#         })

#     @http.route('/unison/unison/objects/<model("unison.unison"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unison.object', {
#             'object': obj
#         })