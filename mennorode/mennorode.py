#!/usr/bin/python3

import argparse
from collections import namedtuple
import inspect
from itertools import chain
import math
import os
import re
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

    def textAt(self, text=None, font_scale=1, left=0, top=0, width=None, height=None):
        match = re.fullmatch(r"^(\d+)(/)(\d+)$", text)
        if match:
            print("{} / {}".format(match.group(1), match.group(3)))
            small_width=width*0.7
            small_height=height*0.5
            small_font=font_scale*0.8
            self.textAt(text=match.group(1), font_scale=small_font, left=left, top=top, width=small_width, height=small_height)
            self.textAt(text="-", font_scale=small_font, left=left+(width-small_width)/2, top=top+(height-small_height)/2, width=small_width, height=small_height)
            self.textAt(text=match.group(3), font_scale=small_font, left=left+width-small_width, top=top+height-small_height, width=small_width, height=small_height)
        else:
            inset = ImageDraw(self.conf, width, height)
            inset.text(text, font_scale)
            inset.edge(stroke_color='red')
            self.composite(inset, left, top)

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

    def edge(self, stroke_color='transparent'):
        self.rectangle(0, 0, self.width, self.height, stroke_color=stroke_color)

    def rotate(self, degrees=30):
        self.image.rotate(degrees)
        self.edge(stroke_color='blue')

    def deform(self, kind):
        self.image.background_color = Color('transparent')
        self.image.virtual_pixel = 'background'
        # print("im({},{})".format(self.image.width, self.image.height))
        args={}
        args['down'] = (
            0, 0, 0, 0,
            0, self.image.height, 0, self.image.height,
            self.image.width, self.image.height, self.image.width, self.image.height,
            self.image.width, 0, self.image.width, self.image.height*1
        )
        args['up'] = (
            0, 0, 0, 0,
            0, self.image.height, 0, self.image.height,
            self.image.width, self.image.height, self.image.width, 0,
            self.image.width, 0, self.image.width, 0
        )
        self.image.distort('bilinear_forward', args[kind])
        self.edge(stroke_color='yellow')

def drawHalfMonth(month, cal, dwg, x, y, xsize, ysize, upper_half):
    print("month={}".format(month))
    l=xsize/math.sqrt(3)
    k=xsize/3.0

    inset = ImageDraw(dwg.conf, l, k)
    # print("l={} k={}".format(l,k))
    inset.edge(stroke_color='green')
    # inset.rectangle(0,0,l,k,stroke_color='green')

    cell_width = l * 0.8 / 7.0
    cell_height = k / 3.0
    for row_index, row in enumerate(cal['months'][month]['cells']):
        if upper_half and row_index < 3:
            continue
        if not upper_half and row_index >= 3:
            continue
        if row_index < 3:
            r_i = row_index
        else:
            r_i = row_index - 3
        for col_index, cell in enumerate(row):
            if 'empty' in cell:
                continue
            value = cell['value']
            inset.textAt(text=value, font_scale=0.8, left=cell_width*col_index, top=cell_height*r_i, width=cell_width, height=cell_height)

    if upper_half:
        inset.deform("down")
        inset.rotate(-30)
        dwg.composite(inset, x, y)
    else:
        inset.deform("up")
        inset.rotate(-30)
        dwg.composite(inset, x, y)

def drawMonth(month, cal, dwg, xpos, ypos, xsize, ysize):
    dwg.rectangle(xpos, ypos, xsize, ysize)
    l=xsize / math.sqrt(3.0)
    k=xsize / 3.0

    inset = ImageDraw(dwg.conf, l, k/2)
    inset.textAt(text=str(cal['year']), font_scale=2, left=0, top=0, width=l, height=k/2)
    inset.rotate(-30)
    dwg.composite(inset, xpos + xsize/2, ypos + 10)

    inset = ImageDraw(dwg.conf, l, k/2)
    inset.textAt(cal['months'][month]['name'], font_scale=2, left=0, top=0, width=l, height=k/2)
    inset.rotate(30)
    dwg.composite(inset, xpos + xsize/2, ypos + 30)

    x = xpos + k
    y = ypos + ysize / 2.0
    drawHalfMonth(month, cal, dwg, x, y, xsize, ysize, True)
    x = xpos + xsize / 2.0
    y = ypos + 2.0 * l
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
   
    with Image() as sequence:
        for page in range(pages):
            sequence.sequence.append(d[page].image)
        sequence.save(filename='mennorode-{}.pdf'.format(str(cal['year'])))

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

