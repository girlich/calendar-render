#!/usr/bin/python3

import argparse
from collections import namedtuple
import inspect
from itertools import chain
import math
import os
import sys
from wand.image import Image
from wand.color import Color
from wand.font import Font
from wand.drawing import Drawing

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from shared import m

class Configuration:
    def __init__(self, dpi=600, font_size=10, text_color='black', font_path='/usr/share/fonts/texlive-gnu-freefont/FreeSans.otf'):
        self.dpi = dpi
        self.font_size = font_size         # in points (72th of an inch)
        self.text_color = text_color 
        self.font_path = font_path

class ImageDraw:
    def __init__(self, conf, width, height):
        self.conf = conf
        self.width = width
        self.height = height
        self.scale = self.conf.dpi/25.4
        self.image = Image(
            width=round(self.width*self.scale),
            height=round(self.height*self.scale),
            background=Color('transparent'),
            resolution=(self.conf.dpi, self.conf.dpi)
        )
        self.image.resolution=self.conf.dpi

    def text(self, text, font_scale):
        with Drawing() as draw:
            # Set the font size, color, and shape
            # draw.font_size = 40
            draw.font_size = round(1.0 * self.conf.font_size * font_scale * self.conf.dpi/72.0)
            draw.text_color = self.conf.text_color
            draw.font = self.conf.font_path

            # Calculate the position to center the text
            font_metrics = draw.get_font_metrics(self.image, text)
            x = round((self.image.width - font_metrics.text_width) / 2)
            text_height = font_metrics.ascender - font_metrics.descender
            # print(font_metrics.ascender, font_metrics.descender, text_height, img.height)
            y = round((self.image.height - text_height) / 2 + font_metrics.ascender)
            # print(y)

            try:
                # Finally Draw the text
                draw.text(x, y, text)
            except:
                print("error printing text '{}' at ({},{})".format(text, x, y))
                pass

            # Apply all drawing operations on the image
            draw(self.image)

    def textAt(self, text=None, font_scale=1, top=0, left=0, width=None, height=None):
        inset = ImageDraw(self.conf, width, height)
        inset.text(text, font_scale)
        inset.rectangle(0,0,width,height)
        self.composite(inset, top, left)

    def composite(self, inset, left, top):
        self.image.composite(
            image=inset.image,
            left=round(left*self.scale),
            top=round(top*self.scale)
        )

    def rectangle(self, x, y, width, height, stroke_color='black'):
        with Drawing() as draw:
            draw.fill_color=Color('transparent')
            draw.stroke_color=Color(stroke_color)
            draw.stroke_width=5
            draw.rectangle(
                left=round(x*self.scale),
                top=round(y*self.scale),
                width=round(width*self.scale),
                height=round(height*self.scale)
            )
            draw(self.image)

    def save(self, filename):
        # print(self.image.resolution)
        self.image.save(filename=filename)

    def rotate(self, degrees=30):
        self.image.rotate(degrees)

    def deformDown(self):
        print(self.image[0][0])
        self.image[0][0]=Color('red')
        for x in range(10):
            for y in range(10):
               self.image[y][x]=Color('red')
        self.image.background_color = Color('transparent')
        self.image.virtual_pixel = 'background'
        Point = namedtuple('Point', ['x', 'y', 'i', 'j'])
        # print("im({},{})".format(self.image.width, self.image.height))
        order = 1.5
        alpha = Point(0, 0, 0, 0)
        beta = Point(0, self.image.height, 0, self.image.height)
        gamma = Point(self.image.width, self.image.height, self.image.width, self.image.height)
        delta = Point(self.image.width, 0, self.image.width, self.image.height*1)
        args = (
            alpha.x, alpha.y, alpha.i, alpha.j,
            beta.x, beta.y, beta.i, beta.j,
            gamma.x, gamma.y, gamma.i, gamma.j,
            delta.x, delta.y, delta.i, delta.j,
        )
        self.image.distort('bilinear_forward', args)

def drawHalfMonth(month, cal, dwg, x, y, xsize, ysize, upper_half):
    print("month={}".format(month))
    cell_width = 4.5
    l=xsize/math.sqrt(3)
    k=xsize/3.0

    inset = ImageDraw(dwg.conf, l, k)
    # print("l={} k={}".format(l,k))
    inset.rectangle(0,0,l,k,stroke_color='green')

    for row_index, row in enumerate(cal['months'][month]['cells']):
        if upper_half and row_index < 3:
            continue
        if not upper_half and row_index >= 3:
            continue
        if row_index < 3:
            r_i = row_index
        else:
            r_i = row_index - 3
        width = 4.5
        for col_index, cell in enumerate(row):
            if 'empty' in cell:
                continue
            value = cell['value']
            inset.textAt(value, 0.9, 0+width*col_index, 0+width*r_i, width, width)

    if upper_half:
        inset.deformDown()
        inset.rotate(-30)
        dwg.composite(inset, x, y)
    else:
        inset.rotate(-30)
        dwg.composite(inset, x, y+k)

def drawMonth(month, cal, dwg, xpos, ypos, xsize, ysize):
    dwg.rectangle(xpos, ypos, xsize, ysize)
    l=xsize/math.sqrt(3)
    k=xsize/3

    inset = ImageDraw(dwg.conf, l, k/2)
    inset.textAt(str(cal['year']), 2, 0, 0, l, k/2)
    inset.rotate(-30)
    dwg.composite(inset, xpos + xsize/2, ypos + 10)

    inset = ImageDraw(dwg.conf, l, k/2)
    inset.textAt(cal['months'][month]['name'], 2, 0, 0, l, k/2)
    inset.rotate(-30)
    dwg.composite(inset, xpos + xsize/2, ypos + 30)

    x = xpos + xsize//2
    y = ypos + ysize//2
    drawHalfMonth(month, cal, dwg, x, y, xsize, ysize, True)
    drawHalfMonth(11-month, cal, dwg, x, y, xsize, ysize, False)


def generatePDF(cal):
    conf=Configuration()

    page_width=210.0    # A4 width in mm
    page_height=297.0   # A4 height in mm

    width=60            # width of a single month
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
        d.append(ImageDraw(conf, page_width, page_height))

    for month in range(months):
        p = month // months_per_page
        i = month%cols
        j = rows - 1 - (month%months_per_page) // cols
        part = (month%months_per_page)
        print("p={} m={} i={} j={} part={}".format(p, month, i, j, part))

        drawMonth(month, cal, d[p], xoffset+i*width, yoffset+j*height, width, height)
    
    for page in range(pages):
        d[page].save('page-{}.pdf'.format(page))

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

