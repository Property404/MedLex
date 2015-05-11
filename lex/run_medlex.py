import lex.ecsv as ecsv
import lex.wordify as wordify
import time
import os


def run(filename, searchdir, columns):
    print("Pulling from "+searchdir+"...")

    # Define variables
    stuff = []
    it = 1  # Iteration control

    # Pull data from files
    for root, sub, files in os.walk(searchdir):
        for csv_file in files:
                grid = ecsv.make_grid_from_csv(root+"/"+csv_file)
                stuff += ecsv.get_columns_from_grid(grid, columns)[1::]
                stuff += ecsv.get_row_from_grid(grid, 0)
                os.sys.stdout.write("\tFiles: {0} with {1} cells   \r".format(str(it), str(len(stuff))))
                it += 1

    # Get words from data
    print("\nGetting words")
    words = wordify.get_words(stuff, exclude=wordify.JUNK_WORDS+wordify.COMMON_WORDS)

    # Create lexicon - 75% scrutiny
    print("Creating lexicon")
    words.sort()
    lexicon = wordify.associate_words(words)

    # Make output
    print("Exporting")
    output = ""
    for group in lexicon:
        for word in group:
            output += word+", "
        output += "\n"

    # Export
    try:
        os.makedirs(os.path.dirname(filename))
    except OSError:
        pass
    fout = open(filename, "w+")
    fout.write(output)
    fout.close()