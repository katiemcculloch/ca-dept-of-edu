import csv
import sys
from doltcli.utils import CREATE, UPDATE
from memory_profiler import profile
import requests
# from bs4 import BeautifulSoup
import doltcli
from print import printWithFilename
import static
from utils import get_content_from_url

def get_tablename_from_args():
    args = sys.argv
    if len(args) < 2:
        print("table name must be provided as argument")
        exit()
    tableName = sys.argv[1]
    return tableName

# def get_content_from_url(tableName):    
#     page = requests.get(static.absentee_urls[tableName])
#     return BeautifulSoup(page.content, 'html.parser')

def createTableIfDoesNotExist():
    lsOutput = db.ls()
    table_already_exists = False
    for table in lsOutput:
        if table.name == tableName:
            table_already_exists = True
    if table_already_exists == False:
        create_table_sql_stmt = ""
        if tableName == "absenteeism_chronic":
            create_table_sql_stmt = "CREATE TABLE `{}` (`academic_year` longtext NOT NULL,`aggregate_level` longtext NOT NULL,`county_code` longtext NOT NULL,`district_code` int unsigned,`school_code` longtext,`county_name` longtext NOT NULL,`district_name` longtext,`school_name` longtext,`charter` longtext NOT NULL,`reporting_category` longtext NOT NULL,`cumulative_enrollment` longtext NOT NULL,`chronic_absenteeism_eligible_cumulative_enrollment` longtext NOT NULL,`chronic_absenteeism_count` longtext NOT NULL,`chronic_absenteeism_rate` longtext NOT NULL, PRIMARY KEY(`academic_year`, `aggregate_level`, `county_code`, `district_code`, `school_code`, `county_name`, `district_name`, `school_name`, `charter`, `reporting_category`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;".format(tableName)
        if tableName == "absenteeism_reason":
            create_table_sql_stmt = "CREATE TABLE `absenteeism_reason` (`academic_year` longtext NOT NULL,`aggregate_level` longtext NOT NULL,`county_code` longtext NOT NULL,`district_code` int unsigned,`school_code` longtext,`county_name` longtext NOT NULL,`district_name` longtext,`school_name` longtext,`charter` longtext NOT NULL,`dass` longtext NOT NULL,`reporting_category` longtext NOT NULL,`eligible_cumulative_enrollment` longtext,`count_of_students_with_one_or_more_absences` longtext,`average_days_absent` longtext,`total_days_absent` longtext NOT NULL,`excused_absences_percent` longtext NOT NULL,`unexcused_absences_percent` longtext NOT NULL,`out_of_school_suspension_absences_percent` longtext NOT NULL,`incomplete_independent_study_absences_percent` longtext NOT NULL,`excused_absences_count` longtext NOT NULL, `unexcused_absences_count` longtext NOT NULL,`out_of_school_suspension_absences_count` longtext NOT NULL,`incomplete_independent_study_absences_count` longtext NOT NULL, PRIMARY KEY(`academic_year`, `aggregate_level`, `county_code`, `county_name`, `charter`, `dass`, `reporting_category`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        print("Creating table `{}`...".format(tableName))
        db.sql(query=create_table_sql_stmt)
    return

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

def formatHeadersOfTxtFile(txtFile):
    all_lines = []
    with open(txtFile) as f:
        all_lines = f.readlines()
        count = 0
        for line in all_lines:
            if count == 0:
                all_lines[0] = mapHeaders(line)
            else:
                all_lines[count] = line.replace("*", "")
            count = count + 1
        f.close()
    with open(txtFile, "w") as f:
        f.writelines(all_lines)
        f.close()
    return

def getYearRangeOfData(txtFile):
    all_lines = []
    with open(txtFile) as f:
        all_lines = f.readlines()
        range = all_lines[1].split()[0]
        f.close()
        return range

def mapHeaders(line):
    result = line
    for word in static.replaceKeywords:
        result = result.replace(word, static.replaceKeywords[word])
    return result

def transformTxtFileToCsv(txtFile, csvFile):
    printWithFilename("Opening {} to read from...", txtFile)
    in_txt = csv.reader(open(txtFile, "r"),delimiter = '\t')

    printWithFilename("Opening {} to write to...", csvFile)
    out_csv = csv.writer(open(csvFile, 'w'))

    printWithFilename("Writing to {}...", csvFile)
    out_csv.writerows(in_txt)

    printWithFilename("Successfully wrote csvFile", csvFile)

@profile
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

@profile
def processURL(tableName, soup):
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
            formatHeadersOfTxtFile(txtFile)
            yearRange = getYearRangeOfData(txtFile)
            
            csvFile = tableName + "-{}".format(yearRange) + ".csv"
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

tableName = get_tablename_from_args()
db = doltcli.Dolt("../../dolt_repos/california-dept-of-education/")
soup = get_content_from_url(static.table_url_map[tableName])
print("Preparing import process for {}...".format(tableName))
createTableIfDoesNotExist()
processURL(tableName, soup)