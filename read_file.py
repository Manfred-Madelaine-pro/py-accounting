import csv


TODO_list = '''
    Given a file name or a repo,
    retreive all data
    and map it to a dictionary
'''

def read_file(file_path):
    with open(file_path, mode='r') as infile:
        reader = csv.reader(infile)
        return [parse(row) for row in reader]


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
    file_path = 'data/Export_00050541037_07022020_06082020.csv'
    read_file(file_path)