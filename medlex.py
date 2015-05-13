#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os
import shutil
import tempfile


# CONSTANTS
VERSION = "0.1.0"

MAN_PAGE = """MedLex

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
   -src <dir>\tUse source path
   -title <str>\tUse title in formatted lexicon
   -upload\tUpload files
   -v\t\tDisplay version number
   -h\t\tPrint Help (this message) and exit
   -l\t\tPrint license and exit
"""
SECRET_MAN_PAGE = """MedLex
Super Secret Help (shh!)

Secret Options:

    -C\t\tImport all modules in lex
    -H\t\tDisplay Secret Help (this message) and exit
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

SETTINGS_LOCATION = os.path.dirname(os.path.realpath(__file__))+"/config.py"

DEFAULT_SETTINGS = """\"\"\"Instructions:
    Change the default variables to customize MedLex.
    You can change the "columns" variable by 'medlex -S'
\"\"\"

# Variables
plaintext_filename_default = "medlex_result.txt"
format_filename_default = "medlex_result.html"
format_title = "Medical Lexicon"
data_destination = \""""+os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\")+"/medlex_hospital_data"+"""\"
data_source = \""""+os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\")+"/medlex_hospital_data"+"""\"
columns = ["HCAHPS Question", "Measure Name", "Footnote Text", "HCAHPS Answer Description"]
"""

# Deal with settings - Ignore warnings
if not os.path.isfile(SETTINGS_LOCATION):
    open(SETTINGS_LOCATION, "w").write(DEFAULT_SETTINGS)
import config
plaintext_filename = config.plaintext_filename_default
format_filename = config.format_filename_default
data_destination = config.data_destination
data_source = config.data_source
columns = config.columns
format_title = config.format_title
upload_source = None
upload_destination = None


temp_folder = tempfile.mkdtemp()+"/"
argv = []
available_flags = "vdrfhlScCFH"
flags = ""


# Concat flags
i = 0
skip_iter = 0

for i in range(len(os.sys.argv)):
    if skip_iter > 0:
        skip_iter -= 1
        continue
    if os.sys.argv[i] == '-upload':
        if len(os.sys.argv) > i+2:
            upload_source = os.sys.argv[i+1]
            upload_destination = os.sys.argv[i+2]
            skip_iter = 2
            continue
        else:
            print("Must give source and destination path for upload")
            print(TRY_HELP)
            exit()
    if os.sys.argv[i] == '-title':
        if len(os.sys.argv) > i+1:
            format_title = os.sys.argv[i+1]
            skip_iter = 1
            continue
        else:
            print("No title given")
            print(TRY_HELP)
            exit()
    if os.sys.argv[i] == '-src':
        if len(os.sys.argv) > i+1:
            data_source = os.sys.argv[i+1]
            skip_iter = 1
            continue
        else:
            print("No source given")
            print(TRY_HELP)
            exit()
    if os.sys.argv[i][0] == '-':
        flags += os.sys.argv[i][1::]
        continue
    argv.append(os.sys.argv[i])
argv.insert(1, "-"+flags)
argc = len(argv)


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
        print(TRY_HELP)
        exit()
    if "C" in flags:
        import lex.download_data
        import lex.run_medlex
        import lex.format_lex
        import lex.sort_csv
        import lex.upload_data
    if "c" in flags:
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
    if "H" in flags:
        print(SECRET_MAN_PAGE)
        exit()
    if "l" in flags:
        print(LICENSE_PAGE)
        exit()
    if "v" in flags:
        print("MedLex "+VERSION+" on Python "+".".join(str(a) for a in os.sys.version_info[0:3]))
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
        # Get columns
        import lex.sort_csv
        column_var = lex.sort_csv.run(data_source)
        # Find and replace
        settings = open(SETTINGS_LOCATION, "r").read()
        a = settings.index("\ncolumns =")+len("\ncolumns =")
        if "\n" in settings[a::]:
            b = a+settings[a::].index("\n")
        else:
            b = len(settings)-1
        settings = settings[0:a]+" "+column_var+settings[b::]
        # Write back to config
        open(SETTINGS_LOCATION, "w").write(settings)
        # Reload settings
        if os.sys.version_info[0] >= 3:
            from importlib import reload
            reload("config")
        print("Done")
    if "d" in flags:
        import lex.download_data
        lex.download_data.download_all_data(temp_path=temp_folder, data_path=data_destination)

if "r" in flags:
    import lex.run_medlex
    lex.run_medlex.run(plaintext_filename, data_source, columns)

if "F" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename, True, format_title)

if "f" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename, False, format_title)

if upload_source is not None:
    from lex.upload_data import upload
    upload(upload_source, upload_destination)

shutil.rmtree(temp_folder)
