# Customer Site Visits — Odoo 17

Source port from the Odoo 19 module. Technical name remains customer_site_visit.
Manifest version: 17.0.1.0.0. Author, maintainer, support, icon, banner and
description assets are preserved. Listing text identifies Odoo 17.

## Compatibility changes

- Menu and test user group fields use groups_id.
- Dashboard JavaScript includes the explicit @odoo-module marker.
- List view architectures and backend view_mode values use tree.
- Photo kanban uses kanban-box and oe_kanban_global_click.
- Form chatter uses the Odoo 17 oe_chatter field layout.
- Dashboard uses check_access_rights and check_access_rule.
- Dashboard action views retain the frontend list type supported by both clients.
- Existing five dashboard/security tests are retained with compatible field names.

## Checks performed

Python syntax, XML parsing, manifest asset/data references, native version-specific
JavaScript transpilation and SCSS compilation passed. Dashboard mounted and
rendered both charts in headless Chrome using this version’s local OWL runtime
and mocked services. This is not a full database-backed browser test.

Full installation, upgrade, PDF and backend tests have not run: the configured
Python environment cannot start the older Odoo runtimes due to missing
dependencies, and the default PostgreSQL role is unavailable.

## Installation

Add the parent odoo17 folder to your Odoo 17 addons_path (or copy this module
into that server’s custom addons directory), update the app list and install
Customer Site Visits. Do not include multiple versions of customer_site_visit
on the same server’s addons_path. No existing database was modified.

On a disposable database with dependencies installed, run your version-specific
odoo-bin with --stop-after-init --no-http --without-demo=all
-i customer_site_visit --test-enable --test-tags /customer_site_visit
and then verify an upgrade with -u customer_site_visit.

This is a source-code port, not a migration or downgrade of Odoo 19 database data.
