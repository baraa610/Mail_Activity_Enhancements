from odoo import api, fields, models, _
from datetime import datetime, time, timedelta, date
import pytz

class MailActivity(models.Model):
    _inherit = "mail.activity"

    # Start date/time for the activity
    date_start = fields.Datetime(
        string="Start Date",
        help="Start date/time of the activity"
    )

    # Duration (in fractional days)
    duration_days = fields.Float(
        string="Duration (Days)",
        compute="_compute_duration_days",
        store=True,
        digits=(16, 6),
        help="Duration from start to end in days (fractional days allowed)"
    )

    _order = "user_id, date_start asc"

    @api.depends("date_start", "date_deadline")
    def _compute_duration_days(self):
        """
        Compute duration in fractional days between date_start and date_deadline.
        - If date_deadline is a date: we assume its end-of-day (23:59:59)
        - If date_deadline is datetime: use it directly
        """
        for rec in self:
            if not rec.date_start or not rec.date_deadline:
                rec.duration_days = 0.0
                continue

            start_dt = rec.date_start
            end_dt = None

            # Convert date_deadline to datetime end-of-day if it's a date
            if isinstance(rec.date_deadline, date) and not isinstance(rec.date_deadline, datetime):
                end_dt = datetime.combine(rec.date_deadline, time.max)
            elif isinstance(rec.date_deadline, datetime):
                end_dt = rec.date_deadline
            elif isinstance(rec.date_deadline, str):
                # Handle cases where it's returned as string
                try:
                    date_obj = fields.Date.from_string(rec.date_deadline)
                    end_dt = datetime.combine(date_obj, time.max)
                except Exception:
                    end_dt = fields.Datetime.from_string(rec.date_deadline)

            # Convert start_dt if it's a string
            if isinstance(start_dt, str):
                start_dt = fields.Datetime.from_string(start_dt)

            if start_dt and end_dt:
                delta = end_dt - start_dt
                rec.duration_days = delta.total_seconds() / 86400.0
            else:
                rec.duration_days = 0.0

    ###########################################################################
    # Daily start reminders
    ###########################################################################
    @api.model
    def send_daily_start_reminders(self, dry_run=False):
        """
        Find activities starting today for each user and send reminder messages.
        """
        MailActivity = self.env["mail.activity"].sudo()
        User = self.env["res.users"]

        users = User.search([])
        sent_summary = {"users": {}, "total_notifications": 0, "details": []}

        for user in users:
            user_tz = user.tz or self.env.context.get("tz") or "UTC"
            try:
                tz = pytz.timezone(user_tz)
            except Exception:
                tz = pytz.UTC

            local_now = datetime.now(tz)
            local_today = local_now.date()
            local_start = tz.localize(datetime.combine(local_today, time.min))
            local_end = tz.localize(datetime.combine(local_today, time.max))

            utc_start = local_start.astimezone(pytz.UTC).replace(tzinfo=None)



class MailActivity(models.Model):
    _inherit = 'mail.activity'

    start_datetime = fields.Datetime(string='Start Date')
    end_datetime = fields.Datetime(string='End Date')

class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    start_datetime = fields.Datetime(string='Start Date')
    end_datetime = fields.Datetime(string="End Date")

    _order = 'activity_user_id, start_datetime asc'
_order = "start_datetime asc, date_deadline asc"