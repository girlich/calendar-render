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
        cell={}
        cell['value']=calendar.day_name[dayOfWeek][:2]
        cell['format']='bold'
        cols.append(cell)
    rows.append(cols)
    cols=[]
    for (dayOfMonth, dayOfWeek) in cal.itermonthdays2(year, month):
        cell={}
        if dayOfMonth != 0:
            cell['value']=str(dayOfMonth)
            cell['justify']='right'
            # cols.append("{:2d}".format(dayOfMonth))
        else:
            cell['empty']=True
        cols.append(cell)
        if dayOfWeek==last:
            rows.append(cols)
            cols=[]
    return rows

def collectYear(year, first, _locale):
    cal={}
    cal['locale'] = _locale
    cal['year'] = year
    cal['months'] = []
    locale.setlocale(locale.LC_ALL, _locale)
    for month in range(1, 13):
        m = {}
        m['name'] = calendar.month_name[month]
        monthArray = collectMonth(year, month, first)
        m['cells'] = monthArray
        cal['months'].append(m)
    return cal

def fillEmptyLines(cal, minLines):
    for month in cal['months']:
        while len(month['cells']) < minLines:
            cols=[]
            for i in range(1,8):
                cell={}
                cell['empty']=True
                cols.append(cell)
            month['cells'].append(cols)
    return cal

def compressShortLines(cal, maxLines):
    for month in cal['months']:
        while len(month['cells']) > maxLines:
            lastLineNumber = len(month['cells'])-1
            for i in range(len(month['cells'][lastLineNumber])):
                if 'value' in month['cells'][lastLineNumber][i]:
                    month['cells'][lastLineNumber-1][i]['value'] += "/" + \
                      month['cells'][lastLineNumber][i]['value']
            month['cells'].pop()
    return cal

def printMonth(month):
    print(" {}".format(month['name']))
    for row in month['cells']:
        line = ""
        width = 5
        for cell in row:
            if 'empty' in cell:
                value = "<>"
            else:
                value = cell['value']
            if 'justify' in cell and cell['justify'] == 'right':
                value = value.rjust(width)
            else:
                value = value.ljust(width)
            line = line + value + " "
        print(line)

def printYear(cal):
    print("{}".format(cal['year']))
    for month in cal['months']:
        printMonth(month)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("--first", help="first day of the week (0=monday)", type=int, default=0)
    parser.add_argument("--locale", help="locale (default de_DE)", type=str, default="de_DE")
    args = parser.parse_args()

    cal=collectYear(args.year, (args.first % 7), args.locale)
    print("ORIG")
    printYear(cal)
    cal=fillEmptyLines(cal, 6)
    print("EMPTY LINES AT END")
    printYear(cal)
    cal=compressShortLines(cal, 6)
    print("COMPRESSED LAST LINE")
    printYear(cal)

if __name__ == "__main__":
    main()

