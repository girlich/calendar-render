#!/usr/bin/python3

import argparse
import calendar
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
    def __init__(self, dpi=600, font_size=10, text_color='black', font_path='/usr/share/fonts/truetype/LiberationSansNarrow-Regular.ttf'):
        self.dpi = dpi
        self.font_size = font_size         # in points (72th of an inch)
        self.text_color = text_color 
        self.font_path = font_path
        self._month_width = None
        self._month_height = None
        self._l = None
        self._k = None
        self._year_font_scale = None
        self._month_font_scale = None
        self._day_font_scale = None

    @property
    def month_width(self):
        """I'm the 'month_width' property."""
        # print("getter of month_width called. Value={}".format(self._month_width))
        return self._month_width

    @month_width.setter
    def month_width(self, value):
        # print("setter of month_width called. Value={}".format(value))
        self._month_width = value
        self.month_height = math.sqrt(3) * self._month_width
        self.l = self.month_height / 3
        self.k = self.month_width / 3

    @month_width.deleter
    def month_width(self):
        # print("deleter of month_width called")
        del self._month_width

    @property
    def month_height(self):
        """I'm the 'month_height' property."""
        # print("getter of month_height called. Value={}".format(self._month_height))
        return self._month_height

    @month_height.setter
    def month_height(self, value):
        # print("setter of month_height called. Value={}".format(value))
        self._month_height = value

    @month_height.deleter
    def month_height(self):
        # print("deleter of month_height called")
        del self._month_height

    @property
    def l(self):
        """I'm the 'l' property."""
        # print("getter of l called. Value={}".format(self._l))
        return self._l

    @l.setter
    def l(self, value):
        # print("setter of l called. Value={}".format(value))
        self._l = value

    @l.deleter
    def l(self):
        # print("deleter of l called")
        del self._l

    @property
    def k(self):
        """I'm the 'k' property."""
        # print("getter of k called. Value={}".format(self._k))
        return self._k

    @k.setter
    def k(self, value):
        # print("setter of k called. Value={}".format(value))
        self._k = value

    @k.deleter
    def k(self):
        # print("deleter of k called")
        del self._k

    @property
    def year_font_scale(self):
        """I'm the 'year_font_scale' property."""
        # print("getter of year_font_scale called. Value={}".format(self._year_font_scale))
        return self._year_font_scale

    @year_font_scale.setter
    def year_font_scale(self, value):
        # print("setter of year_font_scale called. Value={}".format(value))
        self._year_font_scale = value

    @year_font_scale.deleter
    def year_font_scale(self):
        # print("deleter of year_font_scale called")
        del self._year_font_scale

    @property
    def month_font_scale(self):
        """I'm the 'month_font_scale' property."""
        # print("getter of month_font_scale called. Value={}".format(self._month_font_scale))
        return self._month_font_scale

    @month_font_scale.setter
    def month_font_scale(self, value):
        # print("setter of month_font_scale called. Value={}".format(value))
        self._month_font_scale = value

    @month_font_scale.deleter
    def month_font_scale(self):
        # print("deleter of month_font_scale called")
        del self._month_font_scale

    @property
    def day_font_scale(self):
        """I'm the 'day_font_scale' property."""
        # print("getter of day_font_scale called. Value={}".format(self._day_font_scale))
        return self._day_font_scale

    @day_font_scale.setter
    def day_font_scale(self, value):
        # print("setter of day_font_scale called. Value={}".format(value))
        self._day_font_scale = value

    @day_font_scale.deleter
    def day_font_scale(self):
        # print("deleter of day_font_scale called")
        del self._day_font_scale

def newImage(width, height, background, resolution):
    image = Image(
        width=round(width),
        height=round(height),
        background=Color(background),
        resolution=(resolution, resolution)
    )
    image.resolution = resolution
    return image

class ImageDraw:
    def __init__(self, conf, width, height):
        self.conf = conf
        self.width = width
        self.height = height
        self.scale = self.conf.dpi/25.4
        self.image = newImage(
            width=round(self.width*self.scale),
            height=round(self.height*self.scale),
            background='transparent',
            resolution=self.conf.dpi
        )

    def textMetrics(self, text, font_scale):
        with Drawing() as draw:
            draw.font_size = round(1.0 * self.conf.font_size * font_scale * self.conf.dpi/72.0)
            draw.font = self.conf.font_path
            font_metrics = draw.get_font_metrics(self.image, text)
            return (font_metrics.text_width/self.scale, font_metrics.text_height/self.scale)

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
            # inset.edge(stroke_color='red')
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
        # self.edge(stroke_color='blue')

    def deform(self, kind):
        self.image.background_color = Color('transparent')
        self.image.virtual_pixel = 'background'
        args={}
        args['rightdown'] = (
            0, 0, 0, 0,
            0, self.image.height, 0, self.image.height,
            self.image.width, self.image.height, self.image.width, self.image.height,
            self.image.width, 0, self.image.width, self.image.height
        )
        args['rightup'] = (
            0, 0, 0, 0,
            0, self.image.height, 0, self.image.height,
            self.image.width, self.image.height, self.image.width, 0,
            self.image.width, 0, self.image.width, 0
        )
        args['leftdown'] = (
            0, 0, 0, self.image.height,
            0, self.image.height, 0, self.image.height,
            self.image.width, self.image.height, self.image.width, self.image.height,
            self.image.width, 0, self.image.width, 0
        )
        args['leftup'] = (
            0, 0, 0, 0,
            0, self.image.height, 0, 0,
            self.image.width, self.image.height, self.image.width, self.image.height,
            self.image.width, 0, self.image.width, 0
        )
        self.image.distort('bilinear_forward', args[kind])
        # self.edge(stroke_color='yellow')

    def deformPartYear(self):
        imageEmpty = ImageDraw(self.conf, self.width, self.height)
        imageEmpty.image = newImage(width=self.image.width, height=self.image.height, background='transparent', resolution=self.conf.dpi)

        imageLeft = ImageDraw(self.conf, self.width, self.height)
        imageLeft.image = self.image.clone()
        imageLeft.image.crop(0, round(imageLeft.image.height/2), width=round(imageLeft.image.width/2), height=round(imageLeft.image.height/2))
        imageLeft.deform('leftdown')
        imageEmpty.composite(imageLeft, 0, imageEmpty.height/2)

        imageRight = ImageDraw(self.conf, self.width, self.height)
        imageRight.image = self.image.clone()
        imageRight.image.crop(round(imageRight.image.width/2), round(imageRight.image.height/2), width=round(imageRight.image.width/2), height=round(imageRight.image.height/2))
        imageRight.deform('rightdown')
        imageEmpty.composite(imageRight, imageEmpty.width/2, imageEmpty.height/2)

        return imageEmpty

    def deformPartMonth(self):
        imageEmpty = ImageDraw(self.conf, self.width, self.height)
        imageEmpty.image = newImage(width=self.image.width, height=self.image.height, background='transparent', resolution=self.conf.dpi)

        imageLeft = ImageDraw(self.conf, self.width, self.height)
        imageLeft.image = self.image.clone()
        imageLeft.image.crop(0, 0, width=round(imageLeft.image.width/2), height=round(imageLeft.image.height/2))
        imageLeft.deform('leftup')
        imageEmpty.composite(imageLeft, 0, 0)

        imageRight = ImageDraw(self.conf, self.width, self.height)
        imageRight.image = self.image.clone()
        imageRight.image.crop(round(imageRight.image.width/2), 0, width=round(imageRight.image.width/2), height=round(imageRight.image.height/2))
        imageRight.deform('rightup')
        imageEmpty.composite(imageRight, imageEmpty.width/2, 0)

        return imageEmpty

    def tryText(self, text, font_scale_min, font_scale_max, width=None, height=None):
        print("try_text: scale={}..{}, size={}x{}".format(font_scale_min, font_scale_max, width, height))
        (tw, th) = self.textMetrics(text, font_scale_min)
        if tw>width or th>height:
            raise ValueError("scale={}, min text already too large".format(font_scale_min))
        (tw, th) = self.textMetrics(text, font_scale_max)
        if tw<=width and th<=height:
            raise ValueError("scale={}, max text already too small".format(font_scale_max))
        steps = 10
        for i in range(steps):
            font_scale = (font_scale_min + font_scale_max) / 2.0
            (tw, th) = self.textMetrics(text, font_scale)
            print("scale={} {}x{}".format(font_scale, tw, th))
            if tw<=width and th<=height:
                font_scale_min = font_scale
            else:
                font_scale_max = font_scale
        return font_scale_min

def drawHalfMonth(month, cal, dwg, x, y, upper_half):
    print("month={}".format(month))

    inset = ImageDraw(dwg.conf, dwg.conf.l, dwg.conf.k)
    # inset.edge(stroke_color='green')

    cell_width = dwg.conf.l * 0.8 / 7.0
    cell_height = dwg.conf.k / 3.0
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
            inset.textAt(text=value, font_scale=dwg.conf.day_font_scale, left=cell_width*col_index, top=cell_height*r_i, width=cell_width, height=cell_height)
    if upper_half:
        inset.deform("rightdown")
        inset.rotate(-30)
        dwg.composite(inset, x, y)
    else:
        inset.deform("rightup")
        inset.rotate(-30)
        dwg.composite(inset, x, y)

def drawMonth(month, cal, dwg, xpos, ypos):
    dwg.rectangle(xpos, ypos, dwg.conf.month_width, dwg.conf.month_height)

    inset = ImageDraw(dwg.conf, dwg.conf.l, dwg.conf.k)
    inset.textAt(text=str(cal['year']), font_scale=dwg.conf.year_font_scale, left=0, top=dwg.conf.k/2.0, width=dwg.conf.l, height=dwg.conf.k/2.0)
    inset2 = inset.deformPartYear()
    inset2.rotate(-30)
    dwg.composite(inset2, xpos + dwg.conf.k, ypos - dwg.conf.l / 2.0)

    inset = ImageDraw(dwg.conf, dwg.conf.l, dwg.conf.k)
    inset.textAt(cal['months'][month]['name'], font_scale=dwg.conf.month_font_scale, left=0, top=0, width=dwg.conf.l, height=dwg.conf.k/2.0)
    inset2 = inset.deformPartMonth()
    inset2.rotate(30)
    dwg.composite(inset2, xpos + dwg.conf.k, ypos + dwg.conf.l / 2.0)

    x = xpos + dwg.conf.k
    y = ypos + dwg.conf.month_height / 2.0
    drawHalfMonth(month, cal, dwg, x, y, True)

    x = xpos + dwg.conf.month_width / 2.0
    y = ypos + 2.0 * dwg.conf.l
    drawHalfMonth(11-month, cal, dwg, x, y, False)

def generatePDF(cal):
    conf=Configuration()

    page_width=210.0    # A4 width in mm
    page_height=297.0   # A4 height in mm

    conf.month_width=63 # width of a single month
    
    months = 12
    rows = 2
    cols = 3
    months_per_page = rows * cols
    pages = months // months_per_page

    d=[]
    for page in range(pages):
        d.append(ImageDraw(conf, page_width, page_height))

    year_font_scale=d[0].tryText(text=str(cal['year']), font_scale_min=2, font_scale_max=4, width=conf.l, height=conf.k/2.0)
    print("Year font scale={}".format(year_font_scale))
    conf.year_font_scale=year_font_scale

    month_font_scale = 4.0
    for  month in range(months):
        month_font_scale = min(month_font_scale, d[0].tryText(text=cal['months'][month]['name'], font_scale_min=1.8, font_scale_max=4, width=conf.l*0.8, height=conf.k/2.0))
    print("Month font scale={}".format(month_font_scale))
    conf.month_font_scale=month_font_scale

    day_font_scale = 3
    for day in range(1,32):
        day_font_scale = min(day_font_scale, d[0].tryText(text=str(day), font_scale_min=0.7, font_scale_max=3, width=conf.l * 0.8 / 7.0, height=conf.k / 3.0))
    for day in list(calendar.day_name):
        day_font_scale = min(day_font_scale, d[0].tryText(text=day[:2], font_scale_min=0.7, font_scale_max=3, width=conf.l * 0.8 / 7.0, height=conf.k / 3.0))
    print("Day font scale={}".format(day_font_scale))
    conf.day_font_scale=day_font_scale

    xoffset = ( page_width - cols*conf.month_width ) / 2
    yoffset = ( page_height - rows*conf.month_height) / 2

    for month in range(months):
        p = month // months_per_page
        i = month%cols
        j = rows - 1 - (month%months_per_page) // cols
        part = (month%months_per_page)
        print("p={} m={} i={} j={} part={}".format(p, month, i, j, part))

        drawMonth(month=month, cal=cal, dwg=d[p], xpos=xoffset+i*conf.month_width, ypos=yoffset+j*conf.month_height)
   
    with Image() as sequence:
        for page in range(pages):
            sequence.sequence.append(d[page].image)
        sequence.save(filename='mennorode-{}-{}.pdf'.format(str(cal['year']), cal['locale']))

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

