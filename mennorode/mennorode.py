#!/usr/bin/python3

import argparse
import inspect
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
        print(self.scale)
        self.image = Image(
            width=round(self.width*self.scale),
            height=round(self.height*self.scale),
            background=Color('transparent'),
            resolution=(self.conf.dpi, self.conf.dpi)
        )
        self.image.resolution=self.conf.dpi
        print(self.conf.dpi)
        print(self.image.resolution)

    def text(self, text, font_scale):
        with Drawing() as draw:
            # Set the font size, color, and shape
            # draw.font_size = 40
            draw.font_size = round(1.0 * self.conf.font_size * font_scale * self.conf.dpi/72.0)
            print(round(1.0 * self.conf.font_size * font_scale * self.conf.dpi / 72.0))
            draw.text_color = self.conf.text_color
            draw.font = self.conf.font_path

            # Calculate the position to center the text
            font_metrics = draw.get_font_metrics(self.image, text)
            x = round((self.image.width - font_metrics.text_width) / 2)
            text_height = font_metrics.ascender - font_metrics.descender
            # print(font_metrics.ascender, font_metrics.descender, text_height, img.height)
            y = round((self.image.height - text_height) / 2 + font_metrics.ascender)
            # print(y)

            # Finally Draw the text
            draw.text(x, y, text)

            # Apply all drawing operations on the image
            draw(self.image)

    def textAt(self, text=None, font_scale=1, top=0, left=0, width=None, height=None):
        inset = ImageDraw(self.conf, width, height)
        inset.text(text, 1)
        inset.rectangle(0,0,width,height)
        inset.save("klein.pdf")
        self.image.composite(
            image=inset.image,
            left=round(top*self.scale),
            top=round(left*self.scale)
        )

    def rectangle(self, x, y, width, height):
        with Drawing() as draw:
            draw.fill_color=Color('transparent')
            draw.stroke_color=Color('black')
            draw.stroke_width=5
            draw.rectangle(
                left=round(x*self.scale),
                top=round(y*self.scale),
                width=round(width*self.scale),
                height=round(height*self.scale)
            )
            draw(self.image)

    def save(self, filename):
        print(self.image.resolution)
        self.image.save(filename=filename)

def generatePDF(cal):
    conf=Configuration(dpi=300)
    width = 210.0
    height = 297.0
    id = ImageDraw(conf, width, height)
    id.text('Hallo Huhu 1234567890', 1)
    id.rectangle(0,0,width,height)
    id.textAt(text='AAAAAAAAAAAA', font_scale=1, left=10, top=10, width=70, height=30)
    id.save('hallo.pdf')
    

#def drawRectangle(dwg, x, y, width, height):
#    dwg.append(
#        dwg.Rectangle(x, y, width, height,
#            stroke='black',
#            stroke_width=0.5,
#            fill='none'
#        )
#    )

#def drawText(dwg, text, size, justify, x, y, width, height):
#    drawRectangle(dwg, x, y, width, height)
#    if justify=='left':
#        text_anchor='start'
#        xt=x
#    elif justify=='right':
#        text_anchor='end'
#        xt=x+width
#    else:
#        text_anchor='middle'
#        xt=x+width/2
#    yt=y+height/2
#    dwg.append(
#        dwg.Text(text,
#            stroke='black',
#            fill='black',
#            x=xt, y=yt,
#            font_size=size,
#            font_family='sans-serif',
#            font_weight='lighter',
#            dominant_baseline='middle',
#            text_anchor=text_anchor,
#        )
#    )

#def drawTextToImage(filename, text, width, height):
#    print(text)
#    from wand.image import Image
#    from wand.color import Color
#    from wand.font import Font
#    from wand.drawing import Drawing
#    font_size = 40
#    text_color = 'black'
#    font_path = '/usr/share/fonts/texlive-gnu-freefont/FreeSans.otf'
#    with Image(width=width*20, height=height*20, background=Color('transparent')) as img:
#        # Create a drawing context
#        with Drawing() as draw:
#            # Set the font size, color, and shape
#            draw.font_size = font_size
#            draw.text_color = Color(text_color)
#            draw.font = font_path
#
#            # Calculate the position to center the text
#            font_metrics = draw.get_font_metrics(img, text)
#            x = round((img.width - font_metrics.text_width) / 2)
#            text_height = font_metrics.ascender - font_metrics.descender
#            # print(font_metrics.ascender, font_metrics.descender, text_height, img.height)
#            y = round((img.height - text_height) / 2 + font_metrics.ascender)
#            # print(y)
##
#            # Draw the text
#            draw.text(x, y, text)
#
#            # Apply all drawing operations on the image
#            draw(img)
#
#        img.save(filename=filename)
#
#def drawTextImage(dwg, text, size, justify, x, y, width, height):
#    drawRectangle(dwg, x, y, width, height)
#    if justify=='left':
#        text_anchor='start'
#        xt=x
#    elif justify=='right':
#        text_anchor='end'
#        xt=x+width
#    else:
#        text_anchor='middle'
#        xt=x+width/2
#    yt=y+height/2
#    
#    dwg.append(
#        dwg.Text(text,
#            stroke='black',
#            fill='black',
#            x=xt, y=yt,
#            font_size=size,
#            font_family='sans-serif',
#            font_weight='lighter',
#            dominant_baseline='middle',
#            text_anchor=text_anchor,
#        )
#    )
#    filename='tmp.png'
#    drawTextToImage(filename, text, width, height)
#    dwg.append(
#        dwg.Image(x, y, width, height, filename,
#            embed=True
#        )
#    )


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
            # drawText(dwg, value, '10px', justify, x+5*col_index, y+5*row_index, 5, 5)
            drawTextImage(dwg, value, '10px', justify, x+5*col_index, y+5*row_index, 5, 5)

def drawMonth(month, cal, dwg, xpos, ypos, xsize, ysize):
#    drawRectangle(dwg, xpos, ypos, xsize, ysize)
    drawText(dwg, cal['year'], '20px', 'left', xpos + xsize/2, ypos + 10, 30, 15)
    drawText(dwg, cal['months'][month]['name'], '20px', 'left', xpos + xsize/2, ypos + 30, 30, 15)
    x = xpos + xsize//2
    y = ypos + ysize//2
    drawHalfMonth(month, cal, dwg, x, y, True)
    drawHalfMonth(11-month, cal, dwg, x, y, False)


def generateSVG(cal):
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
        d.append(draw.Drawing(page_width, page_height))

    for month in range(months):
        p = month // months_per_page
        i = month%cols
        j = rows - 1 - (month%months_per_page) // cols
        part = (month%months_per_page)
        print("p={} m={} i={} j={} part={}".format(p, month, i, j, part))

        drawMonth(month, cal, d[p], xoffset+i*width, yoffset+j*height, width, height)
    
    for page in range(pages):
        with open('page-{}.svg'.format(page),'w') as writer:
            writer.write(d[page].as_svg())

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

