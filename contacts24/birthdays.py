from contacts24.model import Contact


def print_upcoming_bdays(contacts: list[Contact], days: int = 7):
    print(f"Upcoming birthdays in the next {days} days: for {len(contacts)} contacts")
