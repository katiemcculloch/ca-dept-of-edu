ACADEMIC_YEAR = "academic_year"
AGGREGATE_LEVEL = "aggregate_level"
COUNTY_CODE = "county_code"
DISTRICT_CODE = "district_code"
SCHOOL_CODE = "school_code"
COUNTY_NAME = "county_name"
DISTRICT_NAME = "district_name"
SCHOOL_NAME = "school_name"
CHARTER = "charter"
REPORTING_CATEGORY = "reporting_category"

replaceKeywords = {
    "Academic Year": ACADEMIC_YEAR,
    "AcademicYear": ACADEMIC_YEAR,
    "Aggregate Level": AGGREGATE_LEVEL,
    "AggregateLevel": AGGREGATE_LEVEL,
    "County Code": COUNTY_CODE,
    "CountyCode": COUNTY_CODE,
    "District Code": DISTRICT_CODE,
    "DistrictCode": DISTRICT_CODE,
    "School Code": SCHOOL_CODE,
    "SchoolCode": SCHOOL_CODE,
    "County Name": COUNTY_NAME,
    "CountyName": COUNTY_NAME,
    "District Name": DISTRICT_NAME,
    "DistrictName": DISTRICT_NAME,
    "School Name": SCHOOL_NAME,
    "SchoolName": SCHOOL_NAME,
    "Charter School": CHARTER,
    "CharterYN": CHARTER,
    "DASS": "dass",
    "Reporting Category": REPORTING_CATEGORY,
    "ReportingCategory": REPORTING_CATEGORY,
    "Count of Students with One or More Absences": "count_of_students_with_one_plus_absences",
    "Average Days Absent": "average_days_absent",
    "Total Days Absent": "total_days_absent",
    "Excused Absences (percent)": "excused_absences_percent",
    "Unexcused Absences (percent)": "unexcused_absences_percent",
    "Out-of-School Suspension Absences (percent)": "out_of_school_suspension_absences_percent",
    "Incomplete Independent Study Absences (percent)": "incomplete_independent_study_absences_percent",
    "Excused Absences (count)": "excused_absences_count",
    "Unexcused Absences (count)": "unexcused_absences_count",
    "Out-of-School Suspension Absences (count)": "out_of_school_suspension_absences_count",
    "Incomplete Independent Study Absences (count)": "incomplete_independent_study_absences_count",
    "ï»¿": "",
    "ChronicAbsenteeismEligibleCumulativeEnrollment": "chronic_absenteeism_eligible_cumulative_enrollment",
    "ChronicAbsenteeismCount": "chronic_absenteeism_count",
    "ChronicAbsenteeismRate": "chronic_absenteeism_rate",
    # Must be after ChronicAbsenteeismEligibleCumulativeEnrollment
    "CumulativeEnrollment": "cumulative_enrollment",
    "Eligible Cumulative Enrollment": "eligible_cumulative_enrollment",
}

absentee_urls = {
    "absenteeism_chronic": "https://www.cde.ca.gov/ds/ad/filesabd.asp",
    "absenteeism_reason": "https://www.cde.ca.gov/ds/ad/filesabr.asp"
}