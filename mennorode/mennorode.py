#!/usr/bin/python3

import argparse
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from shared import m

def drawRectangle(dwg, x, y, width, height):
    from svgwrite import mm
    dwg.add(
        dwg.rect((x*mm, y*mm), (width*mm, height*mm),
            stroke='black',
            stroke_width=0.5*mm,
            fill='none'
        )
    )

def drawText(dwg, text, size, justify, x, y, width, height):
    from svgwrite import mm
    drawRectangle(dwg, x, y, width, height)
    if justify=='left':
        text_anchor='start'
        xt=x
    elif justify=='right':
        text_anchor='end'
        xt=x+width
    else:
        text_anchor='middle'
        xt=x+width/2
    yt=y+height/2
    dwg.add(
        dwg.text(text,
            stroke='black',
            fill='black',
            insert=(xt*mm, yt*mm ),
            font_size=size,
            font_family='sans-serif',
            font_weight='lighter',
            text_anchor=text_anchor,
            dominant_baseline='central'
        )
    )

def drawHalfMonth(month, cal, dwg, x, y, upper_half):
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
                justify=cell['justify']
            else:
                justify='left'
            drawText(dwg, value, '10px', justify, x+5*col_index, y+5*row_index, 5, 5)

def drawMonth(month, cal, dwg, xpos, ypos, xsize, ysize):
    drawRectangle(dwg, xpos, ypos, xsize, ysize)
    drawText(dwg, cal['year'], '20px', 'left', xpos + xsize/2, ypos + 10, 30, 15)
    drawText(dwg, cal['months'][month]['name'], '20px', 'left', xpos + xsize/2, ypos + 30, 30, 15)
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

