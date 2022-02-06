#!/usr/bin/python3

import argparse
import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from shared import m

def generateSVG(page):
    import svgwrite
    from svgwrite import cm, mm
    import math
    page_width=210
    page_height=297
    dwg = svgwrite.Drawing('tmp.svg', size=(page_width*mm,page_height*mm))

    rows = 2
    cols = 3

    width=60
    height=width*math.sqrt(3)

    xoffset = ( page_width - cols*width ) / 2
    yoffset = ( page_height - rows*height) / 2

    for i in range(cols):
        for j in range(rows):
            dwg.add(
                dwg.rect(((xoffset+i*width)*mm, (yoffset+j*height)*mm), (width*mm, height*mm),
                    stroke='black',
                    stroke_width=0.5*mm,
                    fill='none'
                )
            )
    dwg.save()

def generatePDF():
    generateSVG(1)
    generateSVG(2)

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
    generatePDF()



if __name__ == "__main__":
    main()

