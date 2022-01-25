#!/usr/bin/python3

import argparse
import calendar
import locale

def collectMonth(year, month, first):
    cal = calendar.Calendar()
    cal.setfirstweekday(first)
    last = (first + 6) % 7
    rows=[]
    cols=[]
    for dayOfWeek in cal.iterweekdays():
        cols.append(calendar.day_name[dayOfWeek][:2])
    rows.append(cols)
    cols=[]
    for (dayOfMonth, dayOfWeek) in cal.itermonthdays2(year, month):
        if dayOfMonth != 0:
            cols.append("{:2d}".format(dayOfMonth))
        else:
            cols.append("  ")
        if dayOfWeek==last:
            line = " ".join(cols)
            rows.append(cols)
            cols=[]
    return rows

def printMonth(rows):
    for row in rows:
        line = ""
        for col in row:
            line = line + col + " "
        print(line)

def collectYear(year, first):
    print("year={} first={}".format(year, first))
    for month in range(1, 13):
        monthArray = collectMonth(year, month, first)
        print("month={}".format(month))
        printMonth(monthArray)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("--first", help="first day of the week (0=monday)", type=int, default=0)
    parser.add_argument("--locale", help="locale (default de_DE)", type=str, default="de_DE")
    args = parser.parse_args()
    locale.setlocale(locale.LC_ALL, args.locale)
    collectYear(args.year, (args.first % 7))

if __name__ == "__main__":
    main()

