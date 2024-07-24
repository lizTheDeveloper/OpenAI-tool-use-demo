
import calendar
from datetime import date
import os

def print_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    s = ""
    for week in cal:
        for day in week:
            if day == 0:
                s += "   "
            else:
                s += "{:>2}".format(day)
        s += "\n"
    print(s)

def main():
    current_date = date.today()
    year = current_date.year
    month = current_date.month

    print_calendar(year, month)

if __name__ == "__main__":
    main()

