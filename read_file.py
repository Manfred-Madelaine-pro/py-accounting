import csv


TODO_list = '''
	Given a file name or a repo,
	retreive all data
	and map it to a dictionary
'''

def read_file(file_path):
	with open(file_path, mode='r') as infile:
	    reader = csv.reader(infile)
        for row in reader:
        	row_parsed = parse(row)
        	# break

def parse(row):
	row = ','.join(row).replace('é', 'e').replace('°', '.').split(';')
	print(f'{len(row)} : {row}')
	return row

if __name__ == '__main__':
	file_path = 'data/Export_00050541037_07022020_06082020.csv'
	read_file(file_path)