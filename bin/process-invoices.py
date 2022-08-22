#!/usr/bin/env python3

# read in all the invoices
# extract the total $ amount
# assign to receivable and receivable:GST

# https://stackoverflow.com/questions/26695903/python-how-to-read-all-files-in-a-directory
from pathlib import Path

import csv
import datetime
import math
import yaml
import json

gst = None

# FIXME: move common functions, such as get_client_data to a module
# so they can be shared among scripts. FOr now, just do a quick'n'dirty
# workaround

with open('receivables.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    files = sorted(Path('.').glob('*.yml'))
    for child in files:
        if child.is_file():
            #print(f"{child.name}:\n{child.read_text()}\n")
            print(f"{child.name}:")
            y = yaml.load(child.read_text(), Loader=yaml.Loader)
            # print("service:", json.dumps(y['service'], indent=4))
            row = [datetime.datetime.strptime(str(y['invoice_date']), '%Y%m%d').strftime('%d/%m/%Y'), y['name']]
            print(y['code'], y['name'])
            print("date:", datetime.datetime.strptime(str(y['invoice_date']), '%Y%m%d').strftime('%d/%m/%Y'))
            #json.dumps(y['invoice_date'], indent=4))
            #print("date:", json.dumps(y['invoice_date'], indent=4))
            amount = 0
            # use the account from the first item
            account = y['service'][0]['account'] 

            for o in y['service']:
                try:
                    # transfer fee doesn't appear on the bank statement so don't include it
                    desc = o['description']
                    if not desc.startswith('Transfer'):
                        amount += o['amount']
                    #print(o['amount'])
                except KeyError:
                    pass
            print('amount:', amount)
            # There is probably a better way to do this
            if y['code'] in ['C4']: # add others to here
                gst = 1.0
            else:
                gst = 1.15

            row.append(round(amount * gst, 2))
            row.append(account)
            print(row)
            writer.writerow(row)

