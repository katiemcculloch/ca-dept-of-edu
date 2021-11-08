import doltcli
import static
from utils import get_tablename_db_and_soup
from cli import get_tablename_from_args
import csv
from doltcli.utils import UPDATE
from memory_profiler import profile
import requests
import doltcli
from print import printWithFilename
import static
from utils import get_tablename_db_and_soup, getATagsWithHref, saveTextFromUrlToTxtFile, transformTxtFileToCsv, writeFileToDolt

def processURL(tableName, db, soup):
    count = 0
    aTagsWithHref = getATagsWithHref(soup)   
    for aTags in aTagsWithHref:
        href = aTags["href"]
        print("\nProcessing {}".format(href))
        if "www3.cde.ca.gov" in href:
            txtFileUrl = href
            txtFile = "{}.txt".format(tableName)
            csvFile = "{}.csv".format(tableName)
            
            saveTextFromUrlToTxtFile(txtFileUrl, txtFile)
            
            csvFile = tableName + "-{}".format(count) + ".csv"
            transformTxtFileToCsv(txtFile, csvFile)

            printWithFilename("Preparing for Dolt import, opening {}", csvFile)
            
            with open(csvFile, 'r') as f:
                commit_msg = "Import of {}".format(csvFile)
                print("commit_msg = ", commit_msg)

                writeFileToDolt(db, tableName, f, UPDATE, commit_msg)

            count = count + 1
        else:
            print("Skipping href not in expected format\n")

    return


tableName, db, soup = get_tablename_db_and_soup()
processURL(tableName, db, soup)