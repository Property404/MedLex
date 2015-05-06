import sys
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    from urllib import urlopen


def format_lex(ifile, ofile, define=False):
    # Get lexicon from file
    lextext = open(ifile, "r").read()
    lex = []
    texts = lextext.split("\n")
    print(texts[0:5])
    for i in texts:
        lex.append(i.split(","))
    print(lex[0:5])

    # Header HTML
    html = """<!DOCTYPE HTML>


    <html>


    <head>
    <title>Medical Lexicon</title>
    </head>


    <body bgcolor="#CCC">
    <style>
    tr:nth-child(even) {background: #DDD}
    tr:nth-child(odd) {background: #CCC}
    </style>

    <h1>Medical Lexicon</h1>
    <h3>Generated by <a href="https://github.com/property404/MedLex">MedLex</a></h3>

    <table>
    <tr><td><strong>Word</strong></td><td><strong>Other forms</strong></td>"""
    if define:
        html += "<td><strong>Definition</strong></td>"
    html += "</tr>\n\n"

    # HTML body
    it = 0
    for i in lex:
        i[0] = i[0].title()

        # If no vowels, it must be all uppercase
        for j in "aeiouy-":
            if j == "-":
                i[0] = i[0].upper()
            if j not in i[0]:
                continue
            break
        it += 1

        sys.stdout.write(str(it)+"/"+str(len(lex))+"\r  ")
        html += "<tr>\n<td>"+i[0]+"</td>\n<td>"
        if len(i) > 1:
            for j in i[1::]:
                if j != i[-1]:
                    html += j
                else:
                    break
                html += "<br>"
        html += "</td>\n"

        if define:
            dsource = urlopen("http://dictionary.reference.com/browse/"+i[0]).read()
            if sys.version_info[0] >= 3:
                dsource = dsource.decode("utf-8")
            definition = ""
            if "Did you mean" not in dsource:
                try:
                    dsource = dsource[dsource.index("<div class=\"def-content\">")::]
                    definition = dsource[0:dsource.index("</div>")+6]
                except:
                    definition = "-"
            html += "<td>"+definition
            html += "</td>"

        html += "\n</tr>\n\n"

    # HTML tail
    html += """</table>
    </body>
    </html>
    """

    # Export
    html = str(u''.join([k if ord(k) < 128 else '' for k in html]))
    f = open(ofile, "w")
    f.write(html)
    f.close()