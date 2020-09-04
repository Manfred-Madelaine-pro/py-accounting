import read_file as rf
import process_data as pcs

TODO_list = '''
    o pick latest file as default 

    o read file
    
    o parse data 
    
    x store data 

    o process data

    x visualize data
'''



if __name__ == '__main__':
    data_dir = 'data/'
    file_path = rf.get_file_path(data_dir)
    parsed_data = rf.read_file(file_path)

    payments_per_month = {}

    # [print(r) for r in parsed_data[1:20]]
    for r in parsed_data[1:]:
        key = '/'.join(r[0].split('/')[1:])
        payments_per_month[key] = payments_per_month.get(key, []) + [r]

    mps = {}
    for month, payments in payments_per_month.items():
       mp = pcs.Monthly_payments(month, payments)
       print(mp)
       mps[mp.date] = mp


    [print (p[:-1]) for p in mps['07/2020'].payments[::-1]]

    payment_carte = [p[2] for p in mps['07/2020'].payments[::-1] if 'ARTE X9372' in p[1]]

    [print(p[:-1]) for p in mps['07/2020'].payments[::-1] if 'ARTE X9372' in p[1]]
    print(sum(payment_carte))
    