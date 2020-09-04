import os
import csv
import glob


TODO_list = '''
    Given a file name or a repo,
    retreive all data
    and map it to a dictionary
'''

ALL_FILES = '*'


def get_file_path(directory):
    # get latest file in directory
    list_of_files = glob.glob(directory + ALL_FILES)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def read_file(file_path):
    def filter_unrelevant(row):
        # True if first character of the row is unexpected 
        return '=' != row[0][0]

    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        return [parse(row) for row in reader if filter_unrelevant(row)]


def parse(row):
    row = ','.join(row).replace('é', 'e').replace('°', '.').split(';')

    row[1] = " ".join(row[1].split())
    row[2] = string_to_float(row[2]) 
    return row


def string_to_float(string):
    string = string.replace(',', '.')
    if '-' in string:
        return - float(string.replace('-', '').replace(',', '.'))
    return float(string) if safe_cast(string, float) else string


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default



if __name__ == '__main__':
    dir = 'data/'
    file_path = dir + 'Export_00050541037_07022020_06082020.csv'
    read_file(file_path)

    res = get_file_path(dir)
    print(res)