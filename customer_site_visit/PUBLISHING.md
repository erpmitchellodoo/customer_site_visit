# Odoo Apps listing

The listing is in `static/description/index.html`. Its Bootstrap 4 grid,
inline styles, system-font stack and local images follow the Odoo Apps
vendor guidance: https://apps.odoo.com/apps/vendor-guidelines
Section links work without JavaScript, external fonts or stylesheets.

## Before submitting

Publisher and maintainer are set to Mitchel Admin, with support at
erpmitchellodoo@gmail.com. The description includes this support contact.
Add a website (`website`) if available and, if sold commercially, price and
currency in `__manifest__.py`. The existing LGPL-3 license is retained.
Review the license and selling terms before submitting through your vendor account.
This task does not publish the module or certify marketplace acceptance.

## Assets

- `banner.png`: generated marketing illustration, not a product screenshot.
- `icon.png`: generated clipboard/building app icon.
- `dashboard.png`: actual dashboard OWL component rendered with illustrative
  fixture data and Bootstrap styling. It is labelled as sample data in the listing;
  it is not a capture of a populated customer database.

Banner generation brief: wide 2:1 Customer Site Visits banner; title
“Customer Site Visits”; subtitle “Plan. Inspect. Follow through.”; CRM, Sales,
Projects labels; aubergine #714B67 and teal #00898C; inspectors, checklist and
commercial building; no fake dashboard, GPS symbols or Odoo logo.

Icon generation brief: white clipboard/checklist and commercial building,
teal checkmarks, rounded aubergine tile, transparent outer canvas, no text.

## Validation performed

- Checked all description image references and section anchors.
- Checked that the description has no scripts, external resources or JS widgets.
- Rendered and visually inspected desktop (1440px) and narrow (500px) previews
  with Bootstrap 4.6.2.
- Reviewed marketing claims against the module source.

The listing describes Sales-based security groups, manager-only dashboard,
planned timestamps and actual duration, signature-image storage, and GPS fields
accurately. Automatic GPS capture, duration variance analytics and PDF photo
galleries are not advertised as implemented.

Installation and business-flow tests were not rerun for these listing-only changes.
