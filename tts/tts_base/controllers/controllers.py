# -*- coding: utf-8 -*-
from odoo import http

# class TtsBase(http.Controller):
#     @http.route('/tts_base/tts_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tts_base/tts_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tts_base.listing', {
#             'root': '/tts_base/tts_base',
#             'objects': http.request.env['tts_base.tts_base'].search([]),
#         })

#     @http.route('/tts_base/tts_base/objects/<model("tts_base.tts_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tts_base.object', {
#             'object': obj
#         })