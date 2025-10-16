# mail_activity_enhancements/__manifest__.py
{
    "name": "Mail Activity Enhancements",
    "version": "17.0.1.0.0",
    "summary": "Add date_start, duration_days, Upcoming filter and daily reminders for mail.activities",
    "description": """
Enhancements for mail.activity:
- date_start (Datetime) for activity start
- duration_days (stored computed)
- 'Upcoming (Mine)' search filter
- Daily reminder cron (per-user timezone support)
""",
    "author": "Mohamed Hussein",
    "website": "https:www.Lynksys.odoo.com",
    "category": "Productivity",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/mail_activity_views.xml",
        "data/mail_activity_templates.xml",
        "data/mail_activity_cron.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
