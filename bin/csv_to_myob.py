#!/usr/bin/env python3
import argparse
import csv
import sys
from functools import partial

parser = argparse.ArgumentParser()
args = None

def parse_args():
    global parser
    global args
    parser.add_argument("infile")
    args = parser.parse_args()
    #print(args.infile)

def get_infile():
    return args.infile

# TODO: these account mappings should be in a data file 
acc = {
'assets:benevolent_bank':('680', 'BNV Bank'),
'(assets:receivables)':('674', 'Accounts Receivable'),
'assets:receivables':('674', 'Accounts Receivable'),
# equity
'(equity:balancing)':('990', 'Balancing'),
'equity:balancing':('990', 'Balancing'),
'equity:shareholders_salaries:donations':('50120', 'Drawings'),
'equity:shareholders_salaries:drawings':('50108', 'Salary'),
'equity:shareholders_salaries:purchases_on_behalf':('50120', 'Drawings'),
'(equity:shareholders_salaries:purchases_on_behalf)':('50120', 'Drawings'),
# income
'income:s:in_data_charges':('23004', 'Sales - Monitoring Systems'),
'income:s:in_web_hosting':('23001', 'Sales - Webhosting'),
'income:s:reimbursement':('23012', 'Disbursements Recovered'),
'income:s:s_in_software_development':('23002', 'Fees - Software Engineering'),
'income:z:z_in_software_development':('900', 'Zero rated Fees - Software Engineering'),
#expenses
'expenses:e:bank_charges':('309', 'Bank charges'),
'expenses:s:computer_equipment':('315', 'Computer Expenses'),
'expenses:s:ex_data_charges':('27004', 'Monitoring Data Services'),
'expenses:s:ex_web_hosting':('29601', 'Webhosting Expenses'),
'expenses:s:insurance':('380', 'Insurance'),
'expenses:s:office':('409', 'Office Expenses'),
'expenses:s:office_equipment':('409', 'Office Expenses'),
'expenses:s:product_development':('27302', 'Product Development Costs'),
'expenses:s:purchases_for_clients':('27102', 'Purchases for clients'),
'expenses:s:regulatory':('302', 'Regulatory Expenses'),
'expenses:s:rent':('427', 'Rent'),
'(expenses:s:s_ex_farm)':('362', 'Farm Expenses'),
'expenses:s:s_subscriptions':('454', 'Subscriptions'),
'expenses:s:software_development':('27002', 'Software Engineering Expenses'),
'expenses:s:telephone':('460', 'Telephone'),
'expenses:s:travel':('464', 'Travelling Expenses'),
'(expenses:s:utilities)':('412', 'Power'),
'expenses:z:mileage':('910', 'Mileage - Zero Rated'),
'(expenses:z:z_cleaning)':('920', 'Cleaning - Zero Rated'),
'(expenses:z:z_ex_farm)':('930','Farm Expenses - Zero Rated'),
'expenses:z:z_internet':('940', 'Internet Expenses - Zero Rated'),
'expenses:z:z_subscriptions':('950', 'Subscriptions - Zero Rated'),
#liabilities
'(liabilities:GST:collected)':('851', 'GST Collected'),
'(liabilities:GST:paid)':('850', 'GST Paid'),
'liabilities:GST to/from IRD':('852', 'GST Payments'),
'liabilities:credit_card':('683', 'ANZ Bank Credit Card'),
'liabilities:payment_tests':('980', 'Payment tests'),
'proportion:s:s_ex_farm':('0', 'Virtual account for splits'),
'proportion:s:utilities':('0', 'Virtual account for splits'),
'proportion:z:z_cleaning':('0', 'Virtual account for splits'),
'proportion:z:z_ex_farm':('0', 'Virtual account for splits')
}

myob_fields = [
    "account code",
    "account name",
    "account type",
    "account type group",
    "tax code",
    "transaction reference",
    "transaction description",
    "transaction date",
    "transaction amount"
]

ledger_fields = [
"txnidx",
"date",
"date2",
"status",
"code",
"description",
"comment",
"account",
"amount",
"commodity",
"credit",
"debit",
"posting-status",
"posting-comment"
]

def get_account_code(line):
    l_field_name = "account"
    acc_name = line[ledger_fields.index(l_field_name)]
    return acc[acc_name][0]

def map_account_name(line):
    l_field_name = "account"
    acc_name = line[ledger_fields.index(l_field_name)]
    return acc[acc_name][1]


# field map from myob field name to ledger field name
fmap = {
    "account code": get_account_code, # needs to return acc["ledger_account_name"]
    "account name": map_account_name,
    "account type": None,
    "account type group": None,
    "tax code": None,
    "transaction reference": None,
    "transaction description": "description",
    "transaction date": "date",
    "transaction amount": "amount"
}

def get_ledger_data(line, myob_field):
    l_field = fmap[myob_field]
    if callable(l_field):
        data = l_field(line)
    elif l_field is None:
        data = ""
    else:
        index = ledger_fields.index(l_field)
        data = line[index]
    return data


def convert_csv(infilename, outfile=sys.stdout):
    #output header
    w = csv.writer(outfile)#, quoting=csv.QUOTE_MINIMAL)
    w.writerow(myob_fields)

    with open(infilename, 'r', encoding='utf-8-sig') as in_file:
        csv_reader = csv.reader(in_file)
        # read the header
        header = csv_reader.__next__()
        #print(header)

        # This will fail if the account isn't defined. This is what we want to happen
        acc_idx = ledger_fields.index("account")
        for line in csv_reader:
            #print(line[acc_idx])
            # This was only needed for the 'other' accounts
            if line[acc_idx].startswith('deductible'):
                print('discarding %s' % line)
                pass
            else:
                w.writerow(map(partial(get_ledger_data, line), myob_fields))

            #print(line[7], acc[line[7]])
    
def main():
    parse_args()
    journal = get_infile()
    convert_csv(journal)

if __name__ == "__main__":
    main()
