# MedLex
MedLex is a tool designed to take in medical data and create a medical lexion
  
**Modules used by MedLex:**

* lex/download_data - Downloads data associated with MedLex  
* lex/ecsv - Easy csv manipulation  
* lex/excel_to_csv - Converts Excel files to CSV  
* lex/format_lex - Beautifies the lexicon as well as adds dictionary definitions  
* lex/run_medlex - Create a medical lexicon  
* lex/scrape - Scrapes webpages  
* lex/vocabulary - List of the 4500 most common English words  
* lex/wordify - Word manpulation  
  
**Packages needed:**

* beautifulsoup4  
* nltk  
* xlrd  
  
**Installation Instructions:**

* [Download](https://github.com/Property404/MedLex/archive/master.zip) and extract
* Install all needed packages through [pip](https://pypi.python.org/pypi/pip) if not installed
* run nltk.download() in python shell if needed
* Optional: Set environmental path variable to include MedLex directory (and Python directory)
* Optional for \*NIX: Type in MedLex directory:
  * mv medlex.py medlex
  * chmod +x medlex

**Usage Instructions:**  

* For usage help, run 'medlex -h'
* If MedLex won't run properly, try [updating Python](https://www.python.org/)
 * MedLex was mostly tested on 2.7.9
 * Also tested on 3.4.3
 * Send feedback to martinez.dagan@gmail.com
