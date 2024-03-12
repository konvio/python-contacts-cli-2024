 def upcoming_birthdays(self, days):
        current_date = datetime.now()
        upcoming_date = current_date + timedelta(days=days)
        upcoming_birthdays = [
            contact["name"] for contact in self.contacts
            if contact["birthday"] and datetime.strptime(contact["birthday"], "%Y-%m-%d").date() <= upcoming_date.date()
        ]
        return upcoming_birthdays
