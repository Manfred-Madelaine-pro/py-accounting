import read_file as rf
import process_data as process


TODO_list = '''
    o pick latest file as default 

    o read file
    
    o parse data 
    
    x store data 

    o process data

    x digest data

    x extract recurrent posts

    x visualize data
'''


DATA_DIR = 'data/'

DATE_ID = 0
LABEL_ID = 1
AMOUNT_ID = 2


def get_payments_per_month(parsed_data):
    payments_per_month = {}
    for r in parsed_data[1:]:
        key = '/'.join(r[DATE_ID].split('/')[1:])
        payments_per_month[key] = payments_per_month.get(key, []) + [r]
    return payments_per_month


def get_all_monthly_payments(payments_per_month):
    mps = {}
    for month, payments in payments_per_month.items():
       mp = process.Monthly_payments(month, payments)
       mps[mp.date] = mp
    return mps


def display(mps):
    [print (p[:-1]) for p in mps['07/2020'].payments[::-1]]

    payment_carte = [p[2] for p in mps['07/2020'].payments[::-1] if 'ARTE X9372' in p[1]]

    [print(p[:-1]) for p in mps['07/2020'].payments[::-1] if 'ARTE X9372' in p[1]]
    print(sum(payment_carte))
    

if __name__ == '__main__':
    file_path = rf.get_file_path(DATA_DIR)

    parsed_data = rf.read_file(file_path)

    payments_per_month = get_payments_per_month(parsed_data)
   
    mps = get_all_monthly_payments(payments_per_month)

    [print(mp) for mp in mps.values()]
    # display(mps)
