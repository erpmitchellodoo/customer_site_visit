from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged
from odoo.tests.common import new_test_user


@tagged('post_install', '-at_install')
class TestSiteVisitDashboard(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].create({'name': 'Dashboard Test Company'})
        cls.other_company = cls.env['res.company'].create({'name': 'Dashboard Other Company'})
        cls.salesperson = new_test_user(
            cls.env, login='visit_dashboard_user', groups='sales_team.group_sale_salesman',
            company_id=cls.company.id, company_ids=[(6, 0, cls.company.ids)], tz='Asia/Dubai')
        cls.manager = new_test_user(
            cls.env, login='visit_dashboard_manager', groups='sales_team.group_sale_manager',
            company_id=cls.company.id,
            company_ids=[(6, 0, (cls.company | cls.other_company).ids)])
        cls.partner = cls.env['res.partner'].create({'name': 'Dashboard Customer', 'is_company': True})
        cls.kind = cls.env['customer.site.visit.type'].create({'name': 'Dashboard Inspection'})
        now = fields.Datetime.now()
        cls.visits = cls.env['customer.site.visit'].create([
            {'partner_id': cls.partner.id, 'visit_type_id': cls.kind.id,
             'user_id': owner, 'company_id': company, 'state': 'planned',
             'planned_start': now - timedelta(days=2), 'planned_end': now - timedelta(days=1)}
            for owner, company in [(cls.salesperson.id, cls.company.id),
                                   (cls.manager.id, cls.company.id),
                                   (cls.salesperson.id, cls.other_company.id)]
        ])
        cls.env['customer.site.visit.finding'].create([
            {'name': 'Overdue action', 'visit_id': visit.id,
             'deadline': fields.Date.today() - timedelta(days=1)} for visit in cls.visits
        ])

    def dashboard(self, user):
        return self.env['customer.site.visit'].with_user(user).with_context(
            allowed_company_ids=self.company.ids, tz='Asia/Dubai').get_dashboard_data()

    def test_sales_user_cannot_access_dashboard(self):
        with self.assertRaises(AccessError):
            self.dashboard(self.salesperson)

    def test_all_documents_user_cannot_access_dashboard(self):
        self.salesperson.write({'group_ids': [(4, self.env.ref(
            'sales_team.group_sale_salesman_all_leads').id)]})
        with self.assertRaises(AccessError):
            self.dashboard(self.salesperson)

    def test_manager_dashboard_respects_enabled_companies(self):
        data = self.dashboard(self.manager)
        self.assertEqual(data['total'], 2)
        self.assertEqual(len(data['findings']), 2)
        self.assertEqual({row['key']: row['count'] for row in data['cards']}['overdue'], 2)
        self.assertNotIn(self.visits[2].id, [row['visit_id'][0] for row in data['findings']])

    def test_card_counts_match_drilldown(self):
        data = self.dashboard(self.manager)
        for card in data['cards']:
            count = self.env[card['model']].with_user(self.manager).with_context(
                allowed_company_ids=self.company.ids).search_count(card['domain'])
            self.assertEqual(card['count'], count)

    def test_dashboard_menu_is_admin_only(self):
        menu = self.env.ref('customer_site_visit.menu_site_visit_dashboard')
        self.assertEqual(menu.group_ids, self.env.ref('sales_team.group_sale_manager'))
