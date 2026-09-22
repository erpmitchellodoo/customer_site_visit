# Customer Site Visit & Inspection Management - Odoo 18

Community-first addon designed to install unchanged on Odoo 18 Community and Enterprise.

## V1
- Site visit lifecycle: Draft, Planned, In Progress, Completed, Cancelled
- Customer/site contact, responsible user and assigned employees
- Visit types with reusable checklist templates
- Check in / check out and actual duration
- Findings and follow-up activities
- Before/during/after photos
- Customer acknowledgement and signature image
- CRM, Sales, Project and Task links with smart buttons
- Calendar and PDF visit report
- Multi-company and chatter/activity support

## Notes
Automatic browser GPS capture is intentionally not included in V1. Latitude/longitude fields are available for integrations and future enhancement.

## Access rights
- Uses the standard Sales groups; no separate Site Visit groups are required.
- Sales users can read, create and edit visits. Own Documents users see visits
  assigned to themselves or unassigned; All Documents users see all visits.
- Sales administrators can also delete visits and manage visit types/checklist templates.
- Visits, checklist entries, findings and photos are restricted to enabled companies;
  detail records follow the responsible user of their parent visit.
- Upgrade `customer_site_visit` after deploying these changes to update existing
  access rights, record rules and menus and remove the former custom groups.

## Dashboard
The Community-compatible **Site Visits > Dashboard** screen includes today's
visits, in-progress visits, overdue visits and overdue follow-ups, clickable
status/type charts, and the next 10 visits and earliest 10 overdue follow-ups.
The dashboard is available only to Sales administrators, with access enforced
on the menu and server endpoint. It has no date or responsible-person filters.
A visit is overdue when its planned end has passed and it is
still Draft, Planned or In Progress. Follow-ups are overdue when their deadline
is before today and the required action remains open.

All counts, lists and drill-down actions use the current user's access rights
and enabled companies. Refresh reloads the data.
Upgrade the module and reload the browser to load the dashboard assets.
