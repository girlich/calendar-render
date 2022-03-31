#!/usr/bin/python3

import datetime
import locale
import string

template_document = r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{longtable}
\pagestyle{empty}
\textwidth20.00cm
\textheight27.5cm
\oddsidemargin-2.0cm
\topmargin-2.8cm
\begin{document}
$tables\end{document}
"""

template_table = r"""\begin{longtable}{|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{1.8cm}|p{7.3cm}|}
\hline
Datum &
Spaziergang &
Gymnastik &
Radfahren &
Schwimmen &
Kommentar \\
\hline
$lines\end{longtable}
\newpage
"""

template_line = r"""\parbox[t]{2.3cm}{$bf$date\vspace{1.16cm}}&&&&&\\
\hline
"""

def format_table(start):
    delta = datetime.timedelta(days=1)
    middle = start+delta*7
    end = start+delta*14
    d = start
    text_lines = ""
    while d<end:
        if d.weekday()>=5:
          bf="\\bf{}"
        else:
          bf=""
        text_lines += string.Template(template_line).substitute(date=d.strftime("%A\\\\%d.%m.%Y"),bf=bf)
        d += delta
        if d == middle:
            text_lines += "\hline"
    text_table = string.Template(template_table).substitute(lines=text_lines)
    return text_table

def format_document(start, pages):
    delta = datetime.timedelta(days=1)
    text_tables = ""
    for page in range(pages):
        d = start + delta * 14 * page
        text_tables += format_table(d)
    text_document = string.Template(template_document).substitute(tables=text_tables)
    return text_document

def main():
    start = datetime.date(2022,3,16)
    pages = 4

    locale.setlocale(locale.LC_ALL, "de_DE")
    text = format_document(start, pages)
    f = open(start.strftime("fortnight-%Y%m%d.tex"),"w")
    f.write(text)
    f.close()

if __name__ == '__main__':
    main()

