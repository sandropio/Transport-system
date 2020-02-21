from odoo import models, fields, api


class Country(models.Model):
    _name = 'tts.location'

    name = fields.Char(string="Name", compute="_compute_name", store=True)
    country_id = fields.Many2one('res.country', string="Country")
    zip = fields.Char(string="Zip")
    city = fields.Char(string="City")

    @api.model
    @api.depends('country_id', 'zip', 'city')
    def _compute_name(self):
        for location in self:
            location.name = ", ".join([location.country_id.name or 'None', location.zip or 'None', location.city or ''])


class Tracking(models.Model):
    _name = 'tts.tracking'

    job_number = fields.Many2one('tts.parcel', string="ნომერი")
    job_no = fields.Char(related="job_number.job_no")
    receiver = fields.Char(related="job_number.receiver")
    sender_organisation_link = fields.Many2one(related="job_number.sender_organisation_link")
    parcel_type = fields.Many2one(related="job_number.parcel_type")
    transport_type_no = fields.Char(related="job_number.transport_type_no")
    contractor = fields.One2many(related="job_number.contractor")
    start_address = fields.Char(related="job_number.start_address")
    start_location = fields.Many2one(related="job_number.start_location")
    end_address = fields.Text(related="job_number.end_address")
    job_status = fields.Selection(related="job_number.job_status")
    job_date = fields.Datetime(related="job_number.job_date")

    notice = fields.Char(string='შენიშვნა')
    parcel_status = fields.Char(selection=[('type1', 'PICKED_UP'), ('type2', 'ARRIVED_TO'), ('type2', 'PROCESSED'),
                                           ('type2', 'DEPARTED'), ('type2', 'IN_TRANSIT'), ('type2', 'DELIVERED')],
                                string='ტვირთის სტატუსი')
    pickup_date = fields.Datetime(string='Pickup თარიღი')

    way_ids = fields.One2many('tts.tracking.way', 'conn_id', string='გზა(გავლილი)')


class Parcel(models.Model):
    _name = 'tts.parcel'
    _rec_name = "job_no"

    weight = fields.Float(string='წონა', digits=(16, 2), required=False, index=True)

    long_meter = fields.Float(string='გრძივი მეტრი', required=False, index=True)
    volume_size = fields.Float(string='მოცულობითი წონა', digits=(16, 2), required=False, index=True)

    description = fields.Text(string='აღწერა', required=False, index=True, translate=True)
    parcel_type = fields.Many2one('tts.parcel.type', 'ტვირთის სახეობა')

    sender_organisation = fields.Char(string='', required=False, index=True, translate=True)
    sender_organisation_link = fields.Many2one('res.partner', domain=[('tts_type', '=', 'sender')], string='ტვირთგამგზავნი')

    packaging_type = fields.Many2one('tts.packaging.type', 'შეფუთვის ტიპი')

    start_location = fields.Many2one('res.country', 'დატვირთვის ქვეყანა')
    start_address = fields.Char(string='დატვირთვის ქალაქი/მის:', required=False, index=True, translate=True)

    end_location = fields.Many2one('res.country', 'დანიშნულების ქვეყანა')
    end_address = fields.Text(string='დანიშნულების ქალაქი/ქვეყანა:', required=False, index=True, translate=True)

    notice = fields.Char(string='შენიშვნა')
    documents = fields.Many2many('ir.attachment', string='დოკუმენტები')

    current_location = fields.Many2one('tts.location', 'მიმდინარე ლოკაცია')
    parcel_status = fields.Char(string='სიგრძე', required=False, index=True, translate=True)

    job_date = fields.Datetime(string="თარიღი")
    job_no = fields.Char(string='ნომერი', required=False, index=True, translate=True)  # თრექინგი


    job_status = fields.Selection(selection=[('type1', 'Type 1'),
                                             ('type2', 'Type 2'), ], string='სტატუსი', default='type1')  # თრექინგი
    customer = fields.Many2one('res.partner', domain=[('tts_type', '=', 'customer')], string="დამკვეთი")
    manager = fields.Many2one('res.users', 'მენეჯერი')
    receive_place = fields.Char(string='მიმღები ქვეყანა', required=False, index=True, translate=True)
    receiver = fields.Char(string='მიმღები', required=False, index=True, translate=True)
    day_num = fields.Char(string='დღეების რაოდ.')

    service_cost = fields.Float(string='ღირებულება', digits=(16, 2), required=False, index=True)
    service_done_date = fields.Datetime(string="")
    service_currency = fields.Many2one('res.currency', 'ვალუტა')

    active_until = fields.Datetime(string="ძალაშია")
    freight_type = fields.Many2one('tts.freight.type', 'გადაზიდვის ტიპი')

    cancel_date = fields.Datetime(string="გაუქმების დრო")

    transport_type_no = fields.Char(string='სატრ. საშ. ნომერი:', required='False', index='True', translate='True')

    pieces_text = fields.Text(string='ნაჭრები', required=False, index=True, translate=True)
    dimension = fields.Char(string='CBM', required=False, index=True, translate=True)
    transport_type = fields.Char(string='ტრანსპორტის ტიპი', required=False, index=True, translate=True)
    full_cargo = fields.Boolean('ფულ კარგო', default=False, store=True)
    service_done_days = fields.Char(string='სერვისის დასრულების დრო', required=False, index=True, translate=True)
    job_create_date = fields.Datetime(string="ჯობის შექმნის დრო")
    shipping_terms = fields.Selection(selection=[('type1', 'Type 1'),
                                                 ('type2', 'Type 2'), ], string='Incoterms', default='type1')
    pickup_date = fields.Datetime(string="Pickup თარიღი")
    weight_dimension = fields.Char(string='წონის განზომილება', required=False, index=True, translate=True)
    cubic_volume = fields.Float(string='კუბური მოცულობა', digits=(16, 2), required=False, index=True)
    job_status_date = fields.Datetime(string="სტატუსის დრო")

    contractor = fields.One2many('tts.contractor', 'connect_id', string='კონტრაქტორი')

    pieces = fields.One2many('tts.pieces', 'connect_id', string='ნაჭრები')

    offer_id = fields.Many2one('tts.offer', string='წინადადება')

    ref_no = fields.Char(string='Ref. No', required=False, index=True, translate=True)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        self.env['tts.tracking'].create({
            'job_number': record.id,
            'pickup_date': record.pickup_date
        })
        return record


class Offer(models.Model):
    _name = 'tts.offer'
    _rec_name = 'offer_no'
    size_unit = fields.Selection(selection=[('type1', 'მ'), ('type2', 'ინჩი'), ], string='ზომის ერთეული',
                                 default='type1')
    length = fields.Char(string='სიგრძე', required=False, index=True, translate=True)
    width = fields.Char(string='სიგანე', required=False, index=True, translate=True)
    height = fields.Char(string='სიმაღლე', required=False, index=True, translate=True)
    weight_unit = fields.Selection(selection=[('type1', 'Type 1'), ('type2', 'Type 2'), ], string='წონის ერთეული',
                                   default='type1')
    weight = fields.Float(string='წონა', digits=(16, 2), required=False, index=True)
    long_meter = fields.Float(string='გრძივი მეტრი', required=False, index=True)
    volume_size = fields.Float(string='მოცულობითი წონა', digits=(16, 2), required=False, index=True)
    parcel_no = fields.Char(string='ნომერი', required=False, index=True, translate=True)
    description = fields.Text(string='აღწერა', required=False, index=True, translate=True)
    parcel_type = fields.Many2one('tts.parcel.type', 'ტვირთის სახეობა')
    sender_organisation = fields.Char(string='', required=False, index=True, translate=True)
    sender_organisation_link = fields.Many2one('res.partner', domain=[('tts_type', '=', 'sender')], string='ტვირთგამგზავნი')
    packaging_type = fields.Many2one('tts.packaging.type', 'შეფუთვის ტიპი')
    start_location = fields.Many2one('res.country', 'დატვირთვის ქვეყანა')
    start_address = fields.Char(string='დატვირთვის ქალაქი/მის:', required=False, index=True, translate=True)
    end_location = fields.Many2one('res.country', 'დანიშნულების ქვეყანა')
    end_address = fields.Text(string='დანიშნულების ქალაქი/ქვეყანა:', required=False, index=True, translate=True)
    notice = fields.Char(string='შენიშვნა')
    current_location = fields.Many2one('tts.location', 'მიმდინარე ლოკაცია')
    parcel_status = fields.Char(string='სიგრძე', required=False, index=True, translate=True)
    offer_date = fields.Datetime(string="თარიღი")
    offer_no = fields.Char(string='ნომერი', required=False, index=True, translate=True)
    offer_status = fields.Selection(selection=[('type1', 'Type 1'), ('type2', 'Type 2'), ], string='სტატუსი',
                                    default='type1')  # თრექინგი
    customer = fields.Many2one('res.partner', domain=[('tts_type', '=', 'customer')], string="დამკვეთი")
    manager = fields.Many2one('res.users', 'მენეჯერი')
    receive_place = fields.Char(string='მიმღები ქვეყანა', required=False, index=True, translate=True)
    receiver = fields.Char(string='მიმღები', required=False, index=True, translate=True)
    day_num = fields.Char(string='დღეების რაოდ.')
    service_cost = fields.Float(string='ღირებულება', digits=(16, 2), required=False, index=True)
    service_done_date = fields.Datetime(string="")
    service_currency = fields.Many2one('res.currency', 'ვალუტა')
    active_until = fields.Datetime(string="ძალაშია")
    freight_type = fields.Many2one('tts.freight.type', 'გადაზიდვის ტიპი')
    cancel_date = fields.Datetime(string="გაუქმების დრო")
    transport_type_no = fields.Char(string='სატრ. საშ. ნომერი:', required='False', index='True', translate='True')
    pieces_text = fields.Text(string='ნაჭრები', required=False, index=True, translate=True)
    dimension = fields.Char(string='CBM', required=False, index=True, translate=True)
    transport_type = fields.Char(string='ტრანსპორტის ტიპი', required=False, index=True, translate=True)
    full_cargo = fields.Boolean('ფულ კარგო', default=False, store=True)
    service_done_days = fields.Char(string='სერვისის დასრულების დრო', required=False, index=True, translate=True)
    job_create_date = fields.Datetime(string="ჯობის შექმნის დრო")
    shipping_terms = fields.Selection(selection=[('type1', 'Type 1'), ('type2', 'Type 2'), ], string='Incoterms',
                                      default='type1')
    pickup_date = fields.Datetime(string="გატანის დრო")
    weight_dimension = fields.Char(string='წონის განზომილება', required=False, index=True, translate=True)
    cubic_volume = fields.Float(string='კუბური მოცულობა', digits=(16, 2), required=False, index=True)
    offer_status_date = fields.Datetime(string="სტატუსის დრო")
    contractor = fields.One2many('tts.contractor', 'conn_id', string='კონტრაქტორი')
    pieces = fields.One2many('tts.pieces', 'connect_id', string='ნაჭრები')
    ref_no = fields.Char(string='Ref. No', required=False, index=True, translate=True)