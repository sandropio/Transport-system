from odoo import models, fields, api
from . import crawler


class DocumentType(models.Model):
    _name = 'tts.document.type'

    type = fields.Char(string='დასახელება', required=False, index=True, translate=True)


class JobDocType(models.Model):
    _inherit = 'ir.attachment'

    doc_type = fields.Many2one('tts.document.type', string='დოკუმენტის ტიპი')
    # browse_document = fields.Many2one('ir.attachment', string='დოკუმენტი')
    note = fields.Char(string='შენიშვნა')


    @api.model
    def upload_document(self):
        files=crawler.my_crawler()
        for addresses in files:

            for file_name in addresses[1::]:
                full_address="/home/davit/uploads/"+file_name
                job_no = addresses[0]

                print(full_address)
                with open(full_address, "rb") as xlfile:
                    byte_data = xlfile.read()
                category_id = self.env['tts.parcel'].search([('job_no', '=', job_no)], limit=1)

                category_id.write({
                    'documents': [(0, 0, {
                        'name': file_name,
                        'datas_fname': file_name,
                        'datas': byte_data,

                    })]
                })







# class Location(models.Model):
#     _name = 'tts.tracking.location'
#
#     loc_ids = fields.Many2one('tts.location', string='მდებარეობა')


class Way(models.Model):
    _name = 'tts.tracking.way'

    location_ids = fields.Many2one('tts.location', string='მდებარეობა')
    way_date = fields.Datetime(string='თარიღი')
    transport_no = fields.Char(string='სატრ.საშ.ნომერი')
    description = fields.Char(string='აღწერა')
    conn_id = fields.Many2one('tts.tracking')
    # connection_id = fields.Many2one('tts.offer')


class JobAccount(models.Model):
    _name = 'tts.job.account'

    account_number = fields.Char(string='ანგარიშის ნომერი')
    bank_name = fields.Char(string='ბანკის დასახელება')
    bic_code = fields.Char(string='BIC')
    account_type = fields.Selection(selection=[('type1', 'საანგარიშსწორებო(მიდმინარე)'), ('type2', 'საკორესპონდენტო'),
                                               ('type3', 'სადეპოზიტო(ანაბარი)'), ('type4', 'მიზნობრივი'),
                                               ('type5', 'სასესხო'), ('type6', 'საბარათე'),
                                               ('type7', 'საკასო მომსახურების')], string='ანგარიშის ტიპი',
                                    default='აირჩიეთ')
    open_date = fields.Datetime(string='გახსნის თარიღი')
    close_date = fields.Datetime(string='დახურვის თარიღი')


class AddContractor(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    # name = fields.Char('სრული სახელი', store=True, compute='_compute_name')
    # # @api.depends('first_name', 'last_name', 'company_name', 'company_type')
    # # def _compute_name(self):
    # #     for partner in self:
    # #         partner.name = (partner.first_name or '') + (partner.last_name or '')

    company_name = fields.Char('კომპანიის სახელი')
    first_name = fields.Char(string='სახელი')
    last_name = fields.Char(string='გვარი')
    id_number = fields.Char(string='პირადი ნომერი')
    mobile_number = fields.Char(string='ტელეფონი')
    email_address = fields.Char(string='ელ.ფოსტა')
    juridical_address = fields.Char(string='იურიდიული მისამართი')
    contact_person = fields.Many2one('res.users', string='საკონტაქტო პირი')
    register_address = fields.Many2one('res.country', string='რეგისტრაციის ადგილი')
    actual_location = fields.Many2one('res.country', string='ფაქტობრივი მდებარეობა')
    actual_address = fields.Char(string='ფაქტობრივი მისამართი')
    business_type = fields.Selection(selection=[('type1', 'activity 1'),
                                                ('type2', 'activity 2')], string='საქმიანობის ტიპი', default='type1')
    job_carrier_type = fields.Many2one('tts.carrier.type', string='გადამზიდავის ტიპი')
    job_account_ids = fields.Many2one('tts.job.account', string='ანგარიში')
    identification_no = fields.Char(string='საიდენტიფიკაციო კოდი')
    contract = fields.Boolean(string='ხელშეკრულება')
    invoice = fields.Many2one('account.invoice', string='ანგარიში')
    user = fields.Many2one('res.users', string='მომხმარებელი')
    tts_type = fields.Selection(selection=[('customer', 'დამკვეთი'),
                                           ('contractor', 'კონტრაქტორი'),
                                           ('sender', 'გამომგზავნი')],)


class InvoiceLines(models.Model):
    _name = 'invoice.lines'

    description = fields.Char(string='აღწერა')
    cost = fields.Char(string='ღირებულება')
    connect_id = fields.Many2one('account.invoice')


class InvoicePayment(models.Model):
    _name = 'invoice.payment'

    payment_person = fields.Selection(selection=[('type1', 'ნაღდი'),
                                                ('type2', 'გადარიცხვა')], string='გადახდის ტიპი')
    tax = fields.Char(string='*გადასახდელი')
    payment_date = fields.Datetime(string='გადახდის თარიღი')
    connect_id = fields.Many2one('account.invoice')


class Invoicing(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    parcel = fields.Many2one('tts.offer', string='*ამანათი')

    @api.onchange('parcel')
    def _on_parcel_change(self):
        self.ensure_one()
        if self.parcel:
            self.partner_id = self.parcel.customer
        else:
            self.partner_id = None

    status = fields.Selection(selection=[('type1', 'წინასწარი'),
                                         ('type2', 'გაცემული'), ('type3', 'ნაწილობრივ გადახდილი'),
                                         ('type4', 'სრულად გადახდილი')], string='*სტატუსი', default='type1')
    full_amount = fields.Float(string='*სულ')
    paid_amount = fields.Float(string='გადახდილი')
    currency = fields.Many2one('res.currency', string='*ვალუტა')
    exchange_rate = fields.Float(string='*კურსი')
    lines = fields.One2many('invoice.lines', 'connect_id', string='სტრიქონები')
    payments = fields.One2many('invoice.payment'
                               '', 'connect_id', string='გადახდები')


class Piece(models.Model):
    _name = 'tts.pieces'

    piece_no = fields.Char(string='ნაჭრის ნომერი')
    note = fields.Char(string='შენიშვნა')
    curr_location = fields.Many2one('tts.location', string='მიმდინარე ლოკაცია')
    quantity = fields.Char(string='რაოდენობა')
    length = fields.Float(string='სიგრძე')
    width = fields.Float(string='სიგანე')
    height = fields.Float(string='სიმაღლე')
    size_unit = fields.Selection(selection=[('m', 'მეტრი'), ('cm', 'სანტიმეტრი')], string='ზომის ერთეული')
    weight = fields.Float(string='წონა')
    weight_unit = fields.Selection(selection=[('kg', 'კილოგრამი'), ('g', 'გრამი')], string='წონის ერთეული')
    long_meter = fields.Float(string='გრძივი მეტრი')
    amount_weight = fields.Float(string='მოცულობითი წონა', compute="weight_sum")
    size_weight = fields.Float(string='ზომა/წონა', digits=(16, 2))

    connect_id = fields.Many2one('tts.offer')

    @api.depends('length', 'width', 'height', 'size_unit')
    def weight_sum(self):
        for record in self:
            if record.size_unit == 'm':
                record.amount_weight = record.length*record.width*record.height/0.006
            else:
                record.amount_weight = record.length*record.width*record.height/6000





class Contractor(models.Model):
    _name = 'tts.contractor'

    supposed_time = fields.Datetime(string='შესრულების სავარაუდო დრო')
    cost = fields.Char(string='ღირებულება')
    currency = fields.Many2one('res.currency', string='ვალუტა')
    contractor = fields.Many2one('res.partner', domain=[('tts_type', '=', 'contractor')], string='კონტრაქტორი')
    transport_type = fields.Selection(selection=[('type1', '20 LCL'), ('type2', '20 FCL'), ('type3', '40 BOXLCL'),
                                                 ('type4', '40 HQLCL'), ('type5', '40 HQ'), ('type6', '45 HQ'),
                                                 ('type7', 'AIR')], string='ტრანსპორტის ტიპი', default='type1')
    connect_id = fields.Many2one('tts.parcel')
    conn_id = fields.Many2one('tts.offer')


class FreightType(models.Model):
    _name = 'tts.freight.type'
    _rec_name = 'code'

    type = fields.Char(string='დასახელება', required=False, index=True, translate=True)
    code = fields.Char(string='კოდი', required=False, index=True, translate=True)


class PackagingType(models.Model):
    _name = 'tts.packaging.type'
    _rec_name = 'type'



    type = fields.Char(string='შეფუთვის სახელი', required=False, index=True, translate=True)


class CarrierType(models.Model):
    _name = 'tts.carrier.type'

    name = fields.Char(string='სახელი', required=False, index=True, translate=True)
    code = fields.Char(string='კოდი', required=False, index=True, translate=True)


class ParcelType(models.Model):
    _name = 'tts.parcel.type'

    name = fields.Char(string='სახელი', required=False, index=True, translate=True)
    dimension = fields.Char(string='სიგრძე', required=False, index=True, translate=True)
