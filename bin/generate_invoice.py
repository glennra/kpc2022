#! /usr/bin/env python3

import argparse
import datetime
import sys
import yaml
from collections import defaultdict
import subprocess
import os

parser = argparse.ArgumentParser()
args = None

def parse_args():
    global parser
    global args
    parser.add_argument("infile")
    parser.add_argument("datadir")
    args = parser.parse_args()
    print(args.infile)
    print(args.datadir)

def get_infile():
    return args.infile

def get_datadir():
    return os.path.join(args.datadir, "data")

def get_templatedir():
    return os.path.join(args.datadir, "templates")

def get_client_data(customer_code):
    with open(os.path.join(get_datadir(),"clients.yml")) as stream:
        d = yaml.load(stream, Loader=yaml.FullLoader)
        # TODO validate data
        #print(d)
        #print(customer_code)
        #print(d[customer_code])
    if(customer_code in d):
        return d[customer_code]
    else:
        raise Exception("customer code %s not found" % customer_code)


def get_my_data():
    with open(os.path.join(get_datadir(),"company.yml")) as stream:
        d = yaml.load(stream, Loader=yaml.FullLoader)
        # TODO validate data
        #print(d)
        return d

def get_layout_data():
    with open(os.path.join(get_templatedir(),"layout.yml")) as stream:
        d = yaml.load(stream, Loader=yaml.FullLoader)
        # TODO validate data
        #print(d)
        return d

def generate_invoice_data():
    # load the invoice data
    infile = get_infile()
    with open(infile, 'r') as stream:
        invoice_data = yaml.load(stream, Loader=yaml.FullLoader)

    # TODO validate data

    # TODO Generate a CSV file for importing into hledger.
    # - I don't think there is another way to do this.
    # - It has the advantage that hledger won't import a transaction more than once.
    # Needs to have fields:
    # "Date","Memo","Amount"
    # There also needs to be a <name>.csv.rules file for the hldeger import

    customer_code = invoice_data["code"]
    #print(customer_code)

    # Transform the date code to human readable form
    date_str = str(invoice_data["invoice_date"])
    print(date_str)
    dd = datetime.datetime
    d = dd.strptime(date_str, "%Y%m%d")
    # human readable date
    invoice_date = d.strftime("%d/%m/%Y")
    print(invoice_date)
    invoice_data["invoice_date"] = invoice_date

    client_data = get_client_data(customer_code)
    print(client_data)

    if client_data["gst_code"] == "S":
        client_data["GST"] = 15
    else:
        client_data["GST"] = 0

    invoice_data["invoice_id"] = date_str+client_data["code"]
    print(invoice_data)

    my_data = get_my_data()
    print(my_data)

    layout_data = get_layout_data()
    print(layout_data)

    # merge dicts
    dicts = [client_data, invoice_data, my_data, layout_data]

    print("merging...")
    # data = defaultdict()

    # for d in dicts:
    #     for k, v in d.items():  # use d.iteritems() in python 2
    #         data[k].add(v)

    data = {}
    for d in dicts:
        data = {**data, **d}

    # Do this after the merge because both invoice_data and data have an "invoice_date" field
    #data["invoice_date"] = invoice_date
    yaml.dump(data, sys.stdout)
    
    outfile = "tmp-details.yml"
    with open(outfile, 'w') as stream:
        stream.write("---\n")
        yaml.dump(data, stream)
        stream.write("---\n")
    # TODO: this could return a stream, without writing the data to disk
    # but it's handy for debugging
    return outfile

def get_outfile_name():
    infile = get_infile()
    return os.path.splitext(infile)[0]+".pdf"


def generate_pdf(datafile, outfile):
    # pandoc --pdf-engine=xelatex details.yml -o output.pdf --template=template.tex
    output = subprocess.check_output(
        ["pandoc", "--pdf-engine=xelatex",
        "--template={}/template.tex".format(get_templatedir()),
        datafile, "-o", outfile])
    print(output)

def main():
    parse_args()
    datafile = generate_invoice_data()
    outfile = get_outfile_name()
    generate_pdf(datafile, outfile)

if __name__ == "__main__":
    main()
