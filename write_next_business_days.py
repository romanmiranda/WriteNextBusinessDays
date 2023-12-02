import sublime
import sublime_plugin
import datetime

class WriteNextBusinessDaysCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Get the current date
        today = datetime.datetime.now()

        # Calculate the remaining business days until Friday
        remaining_business_days = 0

        while today.weekday() < 4:  # Check if today is Friday or a weekend day
            today += datetime.timedelta(days=1)
            remaining_business_days += 1

        # Insert business days at the current cursor position
        cursor_position = self.view.sel()[0].begin() if self.view.sel() else 0
        for _ in range(remaining_business_days, remaining_business_days + 6):  # Print the next 6 business days
            # Skip weekends
            while today.weekday() >= 5:  # Saturday or Sunday
                today += datetime.timedelta(days=1)

            # Print the current business day
            ordinal_day = self.get_ordinal_suffix(today.day)
            row_text = "{0} {1}{2} {3} ====================\n\n\n\n".format(
                today.strftime('%A'), today.day, ordinal_day, today.strftime('%B %Y')
            )
            self.view.insert(edit, cursor_position, row_text)

            # Set cursor position after the last row inserted
            cursor_position = self.view.sel()[0].end()

            today += datetime.timedelta(days=1)

        sublime.status_message("Business days until next Friday added at the cursor position.")

    def get_ordinal_suffix(self, n):
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return suffix
