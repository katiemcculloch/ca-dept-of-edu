import csv
from doltcli.utils import UPDATE
from memory_profiler import profile
import requests
import doltcli
from print import printWithFilename
import static
from utils import get_tablename_db_and_soup, writeFileToDolt, getATagsWithHref, saveTextFromUrlToTxtFile, transformTxtFileToCsv

def createTableIfDoesNotExist(tableName):
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

@profile
def processURL(tableName, soup, db):
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

tableName, db, soup = get_tablename_db_and_soup()
createTableIfDoesNotExist(tableName)
processURL(tableName, soup, db)