import sys

def get_tablename_from_args():
    args = sys.argv
    if len(args) < 2:
        print("\ntable name must be provided as argument after file name, for example:\npython3 absenteeism.py absenteeism_reason\n")
        exit()
    tableName = sys.argv[1]
    return tableName