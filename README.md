# MedLex
MedLex is a tool designed to take in CSV data and create a lexicon
  
**Modules used by MedLex:**

* lex/download_data - Download sample data
* lex/ecsv - Easy csv reading
* lex/excel_to_csv - Convert Excel files to CSV files
* lex/format_lex - Format a lexicon as HTML
* lex/run_medlex - Create a lexicon  
* lex/scrape - Scrape webpages  
* lex/upload_data - Upload files
* lex/vocabulary - List of the 4500 most common English words  
* lex/wordify - Word manipulation  
  
**Packages needed:**

* beautifulsoup4  
* nltk  
* xlrd  
* dropbox
* google-api-python-client
  
**Installation Instructions:**

* [Download](https://github.com/Property404/MedLex/archive/master.zip) and extract
* Install all needed packages through [pip](https://pypi.python.org/pypi/pip) if not installed
* run nltk.download('wordnet') in python shell if needed
* Optional: Set environmental path variable to include MedLex directory
* Optional for \*NIX: Type in MedLex directory:
  * mv medlex.py medlex
  * chmod +x medlex

**Usage Instructions:**  

* For usage help, open doc/Usage Documentation.html
* For additional help, type 'medlex -h'
* If MedLex won't run properly, try [updating Python](https://www.python.org/downloads/)
 * Send feedback to martinez.dagan@gmail.com
