# Mail Activity Enhancements

Enhances **mail.activity** with the following features:

- **date_start** (Datetime) for activity start
- **duration_days** (stored computed)
- **"Upcoming (Mine)"** search filter
- **Daily reminders** (cron) for activities starting today (per-user timezone)

## Installation

1. Place the module folder `mail_activity_enhancements` into your Odoo addons path.
2. Update the Apps list.
3. Install the module from Apps or run via command line.

## Features

- Adds a new start date field for activities.
- Computes activity duration in days.
- Adds a convenient filter to show upcoming activities assigned to the current user.
- Sets up a daily cron job to send reminders for activities starting today, respecting user timezone.

## Dependencies

- Odoo 17+  
- `mail` module

## Author

**Mohamed Hussein**  
Website: [https://www.lynksys.odoo.com](https://www.lynksys.odoo.com)

## License

LGPL-3
