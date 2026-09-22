from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SiteVisitType(models.Model):
    _name = 'customer.site.visit.type'
    _description = 'Site Visit Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    checklist_template_ids = fields.One2many('customer.site.visit.checklist.template', 'visit_type_id', string='Checklist')


class SiteVisitChecklistTemplate(models.Model):
    _name = 'customer.site.visit.checklist.template'
    _description = 'Site Visit Checklist Template'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    visit_type_id = fields.Many2one('customer.site.visit.type', required=True, ondelete='cascade')
    name = fields.Char(required=True)
    required = fields.Boolean(default=False)


class SiteVisit(models.Model):
    _name = 'customer.site.visit'
    _description = 'Customer Site Visit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'planned_start desc, id desc'

    name = fields.Char(default=lambda self: _('New'), readonly=True, copy=False, tracking=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('planned', 'Planned'), ('in_progress', 'In Progress'),
        ('done', 'Completed'), ('cancel', 'Cancelled')], default='draft', required=True, tracking=True)
    visit_type_id = fields.Many2one('customer.site.visit.type', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True, domain="[('is_company','=',True)]")
    contact_id = fields.Many2one('res.partner', string='Site Contact', domain="[('parent_id','=',partner_id)]")
    site_address = fields.Text(compute='_compute_site_address', store=True, readonly=False)
    employee_ids = fields.Many2many('hr.employee', string='Assigned Employees', tracking=True)
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user, tracking=True)
    planned_start = fields.Datetime(required=True, tracking=True, default=fields.Datetime.now)
    planned_end = fields.Datetime(tracking=True)
    check_in = fields.Datetime(readonly=True, tracking=True)
    check_out = fields.Datetime(readonly=True, tracking=True)
    duration_hours = fields.Float(compute='_compute_duration', store=True, string='Actual Duration (Hours)')
    checkin_latitude = fields.Float(digits=(10, 7), readonly=True)
    checkin_longitude = fields.Float(digits=(10, 7), readonly=True)
    checkout_latitude = fields.Float(digits=(10, 7), readonly=True)
    checkout_longitude = fields.Float(digits=(10, 7), readonly=True)
    purpose = fields.Text()
    observations = fields.Html(string='Observations / Findings')
    recommendation = fields.Html(string='Recommendations')
    customer_name = fields.Char(string='Customer Representative')
    customer_comments = fields.Text()
    customer_signature = fields.Image(max_width=1024, max_height=512)
    checklist_ids = fields.One2many('customer.site.visit.checklist', 'visit_id', string='Checklist', copy=True)
    finding_ids = fields.One2many('customer.site.visit.finding', 'visit_id', string='Findings / Follow-up Actions', copy=True)
    photo_ids = fields.One2many('customer.site.visit.photo', 'visit_id', string='Visit Photos', copy=True)
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Opportunity', tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', tracking=True)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    task_id = fields.Many2one('project.task', string='Project Task', tracking=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company, index=True)

    @api.depends('partner_id')
    def _compute_site_address(self):
        for rec in self:
            if rec.partner_id:
                p = rec.partner_id
                rec.site_address = ', '.join(filter(None, [p.street, p.street2, p.city, p.state_id.name, p.zip, p.country_id.name]))
            else:
                rec.site_address = False

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for rec in self:
            rec.duration_hours = ((rec.check_out - rec.check_in).total_seconds() / 3600.0) if rec.check_in and rec.check_out else 0.0

    @api.constrains('planned_start', 'planned_end')
    def _check_planned_dates(self):
        for rec in self:
            if rec.planned_end and rec.planned_start and rec.planned_end < rec.planned_start:
                raise ValidationError(_('Planned end must be after planned start.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('customer.site.visit') or _('New')
        records = super().create(vals_list)
        records._load_checklist_from_type(force=False)
        return records

    def write(self, vals):
        type_changed = 'visit_type_id' in vals
        res = super().write(vals)
        if type_changed:
            self._load_checklist_from_type(force=True)
        return res

    def _load_checklist_from_type(self, force=False):
        Checklist = self.env['customer.site.visit.checklist']
        for rec in self:
            if force:
                rec.checklist_ids.unlink()
            if not rec.checklist_ids and rec.visit_type_id:
                Checklist.create([{
                    'visit_id': rec.id, 'sequence': line.sequence, 'name': line.name, 'required': line.required,
                } for line in rec.visit_type_id.checklist_template_ids])

    def action_plan(self):
        self.write({'state': 'planned'})

    def action_check_in(self):
        for rec in self:
            if rec.state not in ('draft', 'planned'):
                raise UserError(_('Only draft or planned visits can be checked in.'))
            rec.write({'state': 'in_progress', 'check_in': fields.Datetime.now()})

    def action_complete(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError(_('Check in before completing the visit.'))
            missing = rec.checklist_ids.filtered(lambda x: x.required and not x.done)
            if missing:
                raise UserError(_('Complete all required checklist items first: %s') % ', '.join(missing.mapped('name')))
            rec.write({'state': 'done', 'check_out': fields.Datetime.now()})
            rec.finding_ids.filtered(lambda f: f.action_required and f.responsible_id and f.deadline)._schedule_followup()

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_reset_draft(self):
        self.write({'state': 'draft', 'check_in': False, 'check_out': False})

    def action_print_report(self):
        return self.env.ref('customer_site_visit.action_report_site_visit').report_action(self)


class SiteVisitChecklist(models.Model):
    _name = 'customer.site.visit.checklist'
    _description = 'Site Visit Checklist'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    visit_id = fields.Many2one('customer.site.visit', required=True, ondelete='cascade')
    name = fields.Char(required=True)
    required = fields.Boolean(default=False)
    done = fields.Boolean()
    notes = fields.Char()


class SiteVisitFinding(models.Model):
    _name = 'customer.site.visit.finding'
    _description = 'Site Visit Finding / Follow-up'
    _order = 'id'

    visit_id = fields.Many2one('customer.site.visit', required=True, ondelete='cascade')
    name = fields.Char(string='Finding', required=True)
    action_required = fields.Boolean(default=True)
    action = fields.Char(string='Follow-up Action')
    responsible_id = fields.Many2one('res.users')
    deadline = fields.Date()
    done = fields.Boolean()

    def _schedule_followup(self):
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        for line in self:
            if activity_type and line.responsible_id and line.deadline:
                line.visit_id.activity_schedule(
                    activity_type_id=activity_type.id,
                    user_id=line.responsible_id.id,
                    date_deadline=line.deadline,
                    summary=line.action or line.name,
                    note=line.name,
                )


class SiteVisitPhoto(models.Model):
    _name = 'customer.site.visit.photo'
    _description = 'Site Visit Photo'
    _order = 'id desc'

    visit_id = fields.Many2one('customer.site.visit', required=True, ondelete='cascade')
    stage = fields.Selection([('before', 'Before'), ('during', 'During'), ('after', 'After')], default='during', required=True)
    name = fields.Char(string='Caption')
    image = fields.Image(required=True, max_width=1920, max_height=1920)
