#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os
import shutil
import tempfile


# CONSTANTS
MAN_PAGE = """MedLex - Medical Lexicon

usage: medlex [option]
   or: medlex [option] [file]
   or: medlex [option] [txtfile] [htmlfile]

Options:
   -r\t\tMake lexicon
   -d\t\tDownload required medical data
   -f\t\tFormat lexicon
   -F\t\tFormat lexicon with dictionary definitions
   -c\t\tEdit config file
   -S\t\tSort through source data
   -h\t\tPrint Help (this message) and exit
   -l\t\tPrint license and exit
"""

LICENSE_PAGE = """GPL License
Copyright (c) - 2015 Dagan Martinez

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

TRY_HELP = "Try 'medlex -h' for more information"

SETTINGS_LOCATION = os.path.dirname(os.path.realpath(__file__))+"/settings.txt"

DEFAULT_SETTINGS = """[instructions]
    Change the default variables to customize MedLex.\\
    White space is NOT ignored.\\
    You can change the "columns" variable by 'medlex -S'
[/instructions]
[variables]
    [result_default]medlex_result.txt[/result_default]
    [format_default]medlex_result.html[/format_default]
    [data_destination]"""+os.path.dirname(os.path.realpath(__file__))+"/data"+"""[/data_destination]
    [data_source]"""+os.path.dirname(os.path.realpath(__file__))+"/data"+"""[/data_source]
    [columns]HCAHPS Question,Measure Name,Footnote Text,HCAHPS Answer Description[/columns]
[/variables]
"""

# Deal with settings
if os.path.isfile(SETTINGS_LOCATION):
    settings = open(SETTINGS_LOCATION, "r").read()
else:
    settings = DEFAULT_SETTINGS
    open(SETTINGS_LOCATION, "w").write(settings)
get_setting_value = lambda tag_name: settings[settings.index("["+tag_name+"]") +
                                              len(tag_name)+2:settings.index("[/"+tag_name+"]")]
plaintext_filename = get_setting_value("result_default")
format_filename = get_setting_value("format_default")
data_destination = get_setting_value("data_destination")
data_source = get_setting_value("data_source")
columns = get_setting_value("columns").split(",")


temp_folder = tempfile.mkdtemp()+"/"
argv = os.sys.argv
available_flags = "drfhlScF"
flags = ""


# Concat flags
i = 0
for i in range(len(argv)-1):
    if argv[i+1][0] == "-":
        flags += argv[i+1][1::]
    else:
        i -= 1
        break
argv = [argv[0], "-"+flags]+argv[i+2::]
# print(argv)
argc = len(os.sys.argv)


# Check for improper flags
for i in flags:
    if i not in available_flags:
        print("Unknown option: '"+i+"'")
        print(TRY_HELP)
        exit()
flags = ""


# Make sure there are arguments
if argc == 1:
    print("No arguments")
    print(TRY_HELP)
    exit()


# Interpret arguments
if argc > 1:
    if argv[1][0] == "-":
        flags = argv[1]
    else:
        print("No flags. Please use -d, -r, -f, -h, or -l")
        print(TRY_HELP)
        exit()
    if "c" in flags:
        print("Instructions:\n"+get_setting_value("instructions").replace("\n", "").replace("\\", "\n"))
        if os.sys.platform == "win32":
            os.system("notepad "+SETTINGS_LOCATION)
        else:
            if os.system("nano "+SETTINGS_LOCATION):
                if os.system("vi "+SETTINGS_LOCATION):
                    if os.system("vim "+SETTINGS_LOCATION):
                                print("Couldn't find editor")
        exit()
    if "h" in flags:
        print(MAN_PAGE)
        exit()
    if "l" in flags:
        print(LICENSE_PAGE)
        exit()
    if "f" in flags or "F" in flags:
        if argc >= 2:
            if "r" in flags:
                plaintext_filename = temp_folder+plaintext_filename
        if argc >= 3:
            format_filename = argv[2]
        if argc == 4:
            plaintext_filename = argv[2]
            format_filename = argv[3]
        if argc > 4:
            print("Too many arguments\n")
            print(TRY_HELP)
            exit()
    elif "r" in flags:
        if argc == 3:
            plaintext_filename = argv[2]
        elif argc > 3:
            print("Too many arguments\n")
            print(TRY_HELP)
            exit()
    if "S" in flags:
        import lex.sort_csv
        column_xml = lex.sort_csv.run(data_source)
        columns = column_xml.split(",")
        a = settings.index("[columns]")+len("[columns]")
        b = settings.index("[/columns]")
        settings = settings[0:a]+column_xml+settings[b::]
        open(SETTINGS_LOCATION, "w").write(settings)
    if "d" in flags:
        import lex.download_data
        lex.download_data.download_all_data(temp_path=temp_folder, data_path=data_destination)

if "r" in flags:
    import lex.run_medlex
    lex.run_medlex.run(plaintext_filename, data_source, columns)

if "F" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename, True)

if "f" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename)


shutil.rmtree(temp_folder)
