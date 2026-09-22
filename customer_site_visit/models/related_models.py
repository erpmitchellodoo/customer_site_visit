from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    site_visit_ids = fields.One2many('customer.site.visit', 'crm_lead_id', string='Site Visits')
    site_visit_count = fields.Integer(compute='_compute_site_visit_count')
    def _compute_site_visit_count(self):
        for r in self: r.site_visit_count = len(r.site_visit_ids)
    def action_view_site_visits(self):
        return _visit_action(self, [('crm_lead_id', '=', self.id)], {'default_crm_lead_id': self.id, 'default_partner_id': self.partner_id.id})


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    site_visit_ids = fields.One2many('customer.site.visit', 'sale_order_id', string='Site Visits')
    site_visit_count = fields.Integer(compute='_compute_site_visit_count')
    def _compute_site_visit_count(self):
        for r in self: r.site_visit_count = len(r.site_visit_ids)
    def action_view_site_visits(self):
        return _visit_action(self, [('sale_order_id', '=', self.id)], {'default_sale_order_id': self.id, 'default_partner_id': self.partner_id.id})


class ProjectProject(models.Model):
    _inherit = 'project.project'
    site_visit_ids = fields.One2many('customer.site.visit', 'project_id', string='Site Visits')
    site_visit_count = fields.Integer(compute='_compute_site_visit_count')
    def _compute_site_visit_count(self):
        for r in self: r.site_visit_count = len(r.site_visit_ids)
    def action_view_site_visits(self):
        return _visit_action(self, [('project_id', '=', self.id)], {'default_project_id': self.id, 'default_partner_id': self.partner_id.id})


class ProjectTask(models.Model):
    _inherit = 'project.task'
    site_visit_ids = fields.One2many('customer.site.visit', 'task_id', string='Site Visits')
    site_visit_count = fields.Integer(compute='_compute_site_visit_count')
    def _compute_site_visit_count(self):
        for r in self: r.site_visit_count = len(r.site_visit_ids)
    def action_view_site_visits(self):
        return _visit_action(self, [('task_id', '=', self.id)], {'default_task_id': self.id, 'default_project_id': self.project_id.id, 'default_partner_id': self.partner_id.id})


def _visit_action(record, domain, context):
    action = record.env['ir.actions.actions']._for_xml_id('customer_site_visit.action_customer_site_visit')
    action['domain'] = domain
    action['context'] = context
    return action
