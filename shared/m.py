#!/usr/bin/python3

import argparse
import calendar
import locale

def collectMonth(year, month, first):
    print("year={} month={}".format(year, month))
    cal = calendar.Calendar()
    cal.setfirstweekday(first)
    last = (first + 6) % 7
    # print("first={} last={}".format(first, last))
    cols=[]
    for dayOfWeek in cal.iterweekdays():
        cols.append(calendar.day_name[dayOfWeek][:2])
    print(" ".join(cols))
    cols=[]
    for (dayOfMonth, dayOfWeek) in cal.itermonthdays2(year, month):
        if dayOfMonth != 0:
            cols.append("{:2d}".format(dayOfMonth))
        else:
            cols.append("  ")
        if dayOfWeek==last:
            line = " ".join(cols)
            print(line)
            cols=[]

def collectYear(year, first):
    print("year={} first={}".format(year, first))
    for month in range(1, 13):
        collectMonth(year, month, first)

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

