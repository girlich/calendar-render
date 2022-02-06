#!/usr/bin/python3

import argparse
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from shared import m

def drawHalfMonth(month, cal, dwg, x, y, upper_half):
    from svgwrite import mm
    print("month={}".format(month))
    for row_index, row in enumerate(cal['months'][month]['cells']):
        if upper_half and row_index < 3:
            continue
        if not upper_half and row_index >= 3:
            continue
        width = 5
        for col_index, cell in enumerate(row):
            if 'empty' in cell:
                continue
            value = cell['value']
            if 'justify' in cell and cell['justify'] == 'right':
                text_anchor='end'
            else:
                text_anchor='start'
            dwg.add(
                dwg.text(value,
                    stroke='black',
                    fill='black',
                    insert=((x+5*col_index)*mm,(y+5*row_index)*mm),
                    font_size='10px',
                    font_family='sans-serif',
                    font_weight='lighter',
                    text_anchor=text_anchor
                )
            )

def drawMonth(month, cal, dwg, xpos, ypos, xsize, ysize):
    from svgwrite import mm
    dwg.add(
        dwg.rect((xpos*mm, ypos*mm), (xsize*mm, ysize*mm),
            stroke='black',
            stroke_width=0.5*mm,
            fill='none'
        )
    )
    dwg.add(
        dwg.text(cal['year'],
            stroke='black',
            fill='black',
            insert=((xpos + xsize/2)*mm, (ypos + 10)*mm ),
            font_size='20px',
            font_family='sans-serif',
            font_weight='lighter'
        )
    )
    dwg.add(
        dwg.text(cal['months'][month]['name'],
            stroke='black',
            fill='black',
            insert=((xpos + xsize/2)*mm, (ypos + 30)*mm ),
            font_size='20px',
            font_family='sans-serif',
            font_weight='lighter'
        )
    )
    x = xpos + xsize//2
    y = ypos + ysize//2
    drawHalfMonth(month, cal, dwg, x, y, True)
    drawHalfMonth(11-month, cal, dwg, x, y, False)


def generateSVG(cal):
    import svgwrite
    from svgwrite import mm
    import math

    page_width=210
    page_height=297

    width=60
    height=width*math.sqrt(3)
    
    months = 12
    rows = 2
    cols = 3
    months_per_page = rows * cols
    pages = months // months_per_page

    xoffset = ( page_width - cols*width ) / 2
    yoffset = ( page_height - rows*height) / 2

    d=[]
    for page in range(pages):
        d.append(svgwrite.Drawing('page-{}.svg'.format(page), size=(page_width*mm,page_height*mm)))

    for month in range(months):
        p = month // months_per_page
        i = month%cols
        j = rows - 1 - (month%months_per_page) // cols
        part = (month%months_per_page)
        print("p={} m={} i={} j={} part={}".format(p, month, i, j, part))

        drawMonth(month, cal, d[p], xoffset+i*width, yoffset+j*height, width, height)
    
    for page in range(pages):
        d[page].save()

def generatePDF(cal):
    generateSVG(cal)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("--first", help="first day of the week (0=monday)", type=int, default=0)
    parser.add_argument("--locale", help="locale (default de_DE)", type=str, default="de_DE")
    args = parser.parse_args()

    cal=m.collectYear(args.year, (args.first % 7), args.locale)
    print("ORIG")
    m.printYear(cal)
    cal=m.fillEmptyLines(cal, 6)
    print("EMPTY LINES AT END")
    m.printYear(cal)
    cal=m.compressShortLines(cal, 6)
    print("COMPRESSED LAST LINE")
    m.printYear(cal)
    generatePDF(cal)



if __name__ == "__main__":
    main()

