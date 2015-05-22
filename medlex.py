#!/usr/bin/env python
# Copyright (c) - 2015 Dagan Martinez
import os
import shutil
import tempfile


# CONSTANTS
VERSION = "0.2.1"

HELP_PAGE = """MedLex

usage: medlex [option]
   or: medlex [option] [file]
   or: medlex [option] [txtfile] [htmlfile]

Options:
   -r\t\tMake lexicon
   -d\t\tDownload required medical data
   -f\t\tFormat lexicon
   -F\t\tFormat lexicon with dictionary definitions
   -c\t\tEdit config file
   -S\t\tManually sort through source data
   -Z\t\tAutosort through source data
   -src <dir>\tSet source path
   -title <str>\tSet title in formatted lexicon
   -u <f> <dir>\tUpload file
   -upload\tSame as -u
   -L <n>\tLimit files taken into lexicon
   -limit\tSame as -L
   --reset\tReset config
   --version\tPrint version number and exit
   --license\tPrint license and exit
   --help\tPrint Help (this message) and exit
"""
SECRET_HELP_PAGE = """MedLex
Super Secret Help (shh!)

Secret Options:
    -i\t\tImport all modules in lex
    -U\t\tUNIX mode (for Windows)
    -h\t\tPrint Help and exit
    --exhelp\tExport Help and exit
    -H\t\tDisplay Secret Help (this message) and exit
"""

TRY_HELP = "Try 'medlex --help' for more information"
TRY_SECRET_HELP = "Try 'medlex -H' for more information"

LICENSE_LOCATION = os.path.dirname(os.path.realpath(__file__))+"/License"
SETTINGS_LOCATION = os.path.dirname(os.path.realpath(__file__))+"/config.py"

DEFAULT_SETTINGS = """\"\"\"Instructions:
    Change the default variables to customize MedLex.
    You can change the "columns" variable by 'medlex -S' or 'medlex -Z'
\"\"\"

# Variables
plaintext_filename_default = "medlex_result.txt"
format_filename_default = "medlex_result.html"
format_title = "Medical Lexicon"
data_destination = \""""+os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\")+"/medlex_hospital_data"+"""\"
data_source = \""""+os.path.dirname(os.path.realpath(__file__)).replace("\\", "\\\\")+"/medlex_hospital_data"+"""\"
excluded_words = []
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
excluded_words = config.excluded_words

upload_queue = []
limit = 0
temp_folder = tempfile.mkdtemp()+"/"
argv = []
available_flags = "drfhSZciFHU"
flags = ""
unix_mode = False

# Concat flags
i = 0
skip_iter = 0

for i in range(len(os.sys.argv)):
    if skip_iter > 0:
        skip_iter -= 1
        continue
    if os.sys.argv[i] == '--help':
        print(HELP_PAGE)
        exit()
    if os.sys.argv[i] == '--reset':
        os.remove(SETTINGS_LOCATION)
        os.remove(SETTINGS_LOCATION+"c")
        print("Config.py reset")
        open(SETTINGS_LOCATION, "w").write(DEFAULT_SETTINGS)
        continue
    if os.sys.argv[i] == '--exhelp':
        open("HELP PAGE.txt", "w").write(HELP_PAGE.replace("<", "&lt;").replace(">", "&gt;"))
        print("Help page exported")
        exit()
    if os.sys.argv[i] == '--version':
        print("MedLex "+VERSION+" on Python "+".".join(str(a) for a in os.sys.version_info[0:3]))
        exit()
    if os.sys.argv[i] == '--license':
        print(open(LICENSE_LOCATION, 'r').read())
        exit()
    if os.sys.argv[i] == '-limit' or os.sys.argv[i] == '-L':
        if len(os.sys.argv) > i+1:
            limit = int(os.sys.argv[i+1])
            skip_iter = 1
            continue
        else:
            print("Must give file limit")
            print(TRY_SECRET_HELP)
            exit()
    if os.sys.argv[i] == '-upload' or os.sys.argv[i] == '-u':
        if len(os.sys.argv) > i+2:
            upload_queue.append([os.sys.argv[i+1], os.sys.argv[i+2]])
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
    if "U" in flags:
        unix_mode = True
    if "i" in flags:
        import lex.download_data
        import lex.run_medlex
        import lex.format_lex
        import lex.sort_csv
        import lex.upload_data
    if "c" in flags:
        if not unix_mode and os.sys.platform == "win32":
            os.system("notepad \""+SETTINGS_LOCATION+"\"")
        else:
            if os.system("nano \""+SETTINGS_LOCATION+"\""):
                if os.system("vi \""+SETTINGS_LOCATION+"\""):
                    if os.system("vim \""+SETTINGS_LOCATION+"\""):
                                print("Couldn't find editor")
        exit()
    if "h" in flags:
        print(HELP_PAGE)
        exit()
    if "H" in flags:
        print(SECRET_HELP_PAGE)
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
    if "d" in flags:
        import lex.download_data
        lex.download_data.download_all_data(temp_path=temp_folder, data_path=data_destination)
    if "S" in flags or "Z" in flags:
        # Get columns
        import lex.sort_csv
        column_var = lex.sort_csv.run(data_source, limit, "Z" in flags)
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
            reload(config)
        print("Done")


if "r" in flags:
    import lex.run_medlex
    lex.run_medlex.run(plaintext_filename, data_source, columns, limit, excluded_words)

if "F" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename, True, format_title)

if "f" in flags:
    import lex.format_lex
    lex.format_lex.format_lex(plaintext_filename, format_filename, False, format_title)

if upload_queue is not []:
    from lex.upload_data import upload
    for upload_data in upload_queue:
        destinations = upload_data[1].split(";")
        for path in destinations:
            upload(upload_data[0], path)

shutil.rmtree(temp_folder)
