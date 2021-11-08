from bs4 import BeautifulSoup
import requests
import doltcli
import static
from cli import get_tablename_from_args
from print import printWithFilename
import csv

def get_content_from_url(url):    
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_tablename_db_and_soup():
    tableName = get_tablename_from_args()
    print("Preparing import process for {}...".format(tableName))
    db = doltcli.Dolt("../../dolt_repos/california-dept-of-education/")
    soup = get_content_from_url(static.table_url_map[tableName])
    return tableName, db, soup

def getATagsWithHref(soup):
    tableRows = soup.find_all("td")
    asWithHref = []
    for row in tableRows:
        asWithHref.extend(row.find_all("a", href=True))
    return asWithHref

def saveTextFromUrlToTxtFile(txtFileUrl, txtFile):
    lines = requests.get(txtFileUrl).text
    printWithFilename("Writing lines from response to {}...", txtFile)
    with open(txtFile, 'w') as f:
        f.write(lines)
        f.close()
    return

def transformTxtFileToCsv(txtFile, csvFile):
    printWithFilename("Opening {} to read from...", txtFile)
    in_txt = csv.reader(open(txtFile, "r"),delimiter = '\t')

    printWithFilename("Opening {} to write to...", csvFile)
    out_csv = csv.writer(open(csvFile, 'w'))

    printWithFilename("Writing to {}...", csvFile)
    out_csv.writerows(in_txt)

    printWithFilename("Successfully wrote csvFile", csvFile)

def writeFileToDolt(db, tableName, file_handle, import_mode, commit_msg):
    doltcli.write_file(
        dolt=db,
        table=tableName,
        file_handle=file_handle,
        import_mode=import_mode,
        commit=True,
        commit_message=commit_msg,
        continue_import_on_bad_row=True
    )
    return