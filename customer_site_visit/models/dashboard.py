from datetime import datetime, time, timedelta

import pytz

from odoo import api, fields, models, _
from odoo.exceptions import AccessError


class SiteVisitDashboard(models.Model):
    _inherit = 'customer.site.visit'

    @api.model
    def get_dashboard_data(self):
        """Aggregate with the caller's ACLs, record rules and enabled companies."""
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise AccessError(_('Only Sales administrators can access the Site Visit dashboard.'))
        self.check_access_rights('read')
        self.check_access_rule('read')
        timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')

        def midnight(day):
            local = timezone.localize(datetime.combine(day, time.min))
            return fields.Datetime.to_string(local.astimezone(pytz.UTC).replace(tzinfo=None))

        domain = []
        now = fields.Datetime.now()
        today = fields.Date.context_today(self)
        unfinished = [('state', 'in', ['draft', 'planned', 'in_progress'])]
        today_domain = domain + [('planned_start', '>=', midnight(today)),
                                 ('planned_start', '<', midnight(today + timedelta(days=1)))]
        progress_domain = domain + [('state', '=', 'in_progress')]
        overdue_domain = domain + unfinished + [('planned_end', '<', now)]
        upcoming_domain = domain + [('state', 'in', ['draft', 'planned']), ('planned_start', '>=', now)]
        finding_domain = [('visit_id', 'any', domain), ('action_required', '=', True),
                          ('done', '=', False), ('deadline', '<', today)]
        Finding = self.env['customer.site.visit.finding']
        cards = [
            {'key': key, 'label': label, 'count': model.search_count(card_domain),
             'model': model._name, 'domain': card_domain}
            for key, label, model, card_domain in [
                ('today', _("Today's Visits"), self, today_domain),
                ('progress', _('In Progress'), self, progress_domain),
                ('overdue', _('Overdue Visits'), self, overdue_domain),
                ('followups', _('Overdue Follow-ups'), Finding, finding_domain),
            ]
        ]
        counts = dict(self._read_group(domain, ['state'], ['__count']))
        statuses = [{'key': key, 'label': label, 'count': counts.get(key, 0),
                     'domain': domain + [('state', '=', key)]}
                    for key, label in self._fields['state']._description_selection(self.env)]
        types = [{'key': kind.id, 'label': kind.display_name, 'count': count,
                  'domain': domain + [('visit_type_id', '=', kind.id)]}
                 for kind, count in self._read_group(domain, ['visit_type_id'], ['__count'])]
        return {
            'cards': cards, 'statuses': statuses, 'types': types,
            'total': sum(counts.values()), 'domain': domain,
            'upcoming_domain': upcoming_domain, 'finding_domain': finding_domain,
            'upcoming': self.search_read(upcoming_domain,
                ['name', 'partner_id', 'user_id', 'planned_start'], limit=10, order='planned_start, id'),
            'findings': Finding.search_read(finding_domain,
                ['name', 'visit_id', 'responsible_id', 'deadline'], limit=10, order='deadline, id'),
        }
