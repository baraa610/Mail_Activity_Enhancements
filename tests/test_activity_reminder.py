# mail_activity_enhancements/tests/test_activity_reminder.py
from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta
from odoo import fields

class TestMailActivityReminder(TransactionCase):
    def setUp(self):
        super().setUp()
        self.User = self.env['res.users']
        self.Activity = self.env['mail.activity']
        # create a test user
        self.user = self.User.create({
            'name': 'Test User',
            'login': 'testuser',
            'email': 'test@example.com',
            'tz': 'UTC'
        })

    def test_duration_and_reminder(self):
        # create an activity that starts today and ends in 2 days
        today_utc = fields.Datetime.context_timestamp(self.env, fields.Datetime.now()).date()
        # set date_start = now UTC
        start_dt = fields.Datetime.to_string(fields.Datetime.now())
        # set date_deadline as a Date 2 days from today
        deadline_date = fields.Date.to_string(fields.Date.context_today(self.env) + timedelta(days=2))

        activity = self.Activity.create({
            'res_model': 'res.partner',
            'res_id': self.env.ref('base.res_partner_1').id if self.env.ref('base.res_partner_1', False) else False,
            'user_id': self.user.id,
            'summary': 'Test activity',
            'date_start': start_dt,
            'date_deadline': deadline_date,
        })

        # recompute stored fields
        activity._compute_duration_days()
        # duration_days should be > 0 (approx 2 days minus small delta)
        self.assertTrue(activity.duration_days >= 1.9)

        # call the reminder in dry_run
        result = self.Activity.send_daily_start_reminders(dry_run=True)
        # result should include our user
        self.assertIn(self.user.login or self.user.name, result['users'])
