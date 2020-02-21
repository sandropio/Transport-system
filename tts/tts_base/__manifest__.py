# -*- coding: utf-8 -*-
{
    'name': "TTS base",
    'summary': """
    """,
    'description': """
    """,
    'author': "Innosoft",
    'website': "http://www.yourcompany.com",
    'category': 'Innosoft',
    'version': '1.0',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/jobs.xml',
        'views/invoice.xml',
        'views/templates.xml',
        'views/manager.xml',
        'views/partner.xml',
        'views/offers.xml',
        'views/tracking.xml',
        'data/tts_cronjob.xml'


    ],
}