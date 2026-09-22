{
    'name': 'Customer Site Visits',
    'version': '19.0.1.0.1',
    'summary': 'Site visits, inspections, checklists and follow-ups linked to CRM, Sales and Projects',
    'description': '''
Plan and document customer site visits in Odoo 19.
Manage visit checklists, check-in/check-out, actual duration, findings,
follow-up activities, staged photographs and customer acknowledgement.
Link visits to CRM opportunities, sales orders, projects and tasks.
Includes a manager dashboard, calendar, PDF report and multi-company rules.
GPS coordinate fields are available; automatic GPS capture is not included.
''',
    'images': ['static/description/banner.png'],
    'category': 'Services/Project',
    'author': 'Mitchel Admin',
    'maintainer': 'Mitchel Admin',
    'support': 'erpmitchellodoo@gmail.com',
    'license': 'LGPL-3',
    'depends': ['web', 'mail', 'crm', 'sale_management', 'project', 'hr'],
    'assets': {
        'web.assets_backend': [
            'customer_site_visit/static/src/dashboard/dashboard.js',
            'customer_site_visit/static/src/dashboard/dashboard.xml',
            'customer_site_visit/static/src/dashboard/dashboard.scss',
        ],
    },
    'data': [
        'security/site_visit_security.xml',
        'security/ir.model.access.csv',
        'data/site_visit_sequence.xml',
        'data/site_visit_types.xml',
        'views/site_visit_type_views.xml',
        'views/site_visit_views.xml',
        'views/related_document_views.xml',
        'views/site_visit_menus.xml',
        'report/site_visit_report.xml',
        'report/site_visit_report_template.xml',
    ],
    'application': True,
    'installable': True,
}
