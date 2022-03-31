#!/usr/bin/python3

import datetime
import locale
import string

text_start = r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{longtable}
\textwidth20.00cm
\textheight27.5cm
\oddsidemargin-2.0cm
\topmargin-2.5cm
\begin{document}
\begin{longtable}{|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{7.3cm}|}
\hline
Datum &
Spaziergang &
Gymnastik &
Radfahren &
Schwimmen &
Kommentar \\
\hline
"""

text_line = r"""\parbox[t]{2.3cm}{$bf$date\vspace{1.16cm}}&&&&&\\
\hline
"""

text_end = r"""\endhead
\end{longtable}
\end{document}
"""

def onepage(start):
    locale.setlocale(locale.LC_ALL, "de_DE")
    delta = datetime.timedelta(days=1)
    middle = start+delta*7
    end = start+delta*14
    d = start
    f = open(start.strftime("page-%Y-%m-%d.tex"), "w")
    f.write(text_start)
    t = string.Template(text_line)
    while d<end:
        if d.weekday()>=5:
          bf="\\bf{}"
        else:
          bf=""
        f.write(t.substitute(date=d.strftime("%A\\\\%d.%m.%Y"),bf=bf))
        d += delta
        if d == middle:
          f.write("\hline")
    f.write(text_end)
    f.close()

def main():
    onepage(datetime.date(2022,3,16))
    onepage(datetime.date(2022,3,30))

if __name__ == '__main__':
    main()

