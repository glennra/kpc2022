# kpc2022

This is the sample data and code from my Kiwi PyCon XI (2022) talk "Plain text accounting for fun and profit".

I use this for creating invoices, calculating GST and preparing data for my accountant. It is specifically for New Zealand but I suppose it could easily be adapted for another country.

References:

* [plaintextaccounting.org](https://plaintextaccounting.org)

* [hledger.org](https://hledger.org)

## Prerequisites

[```hledger```](https://hledger.org), Python 3 and PyYAML.

## Creating invoices

The contact information "database" is in the ```data``` directory.

Your company information goes in the ```company.yml``` file.

Put your client info in the ```clients.yml``` file. The client code can be any valid two character Python dict key.

There is also a ```suppliers.yml``` file that is currently unused.

Invoice data goes in a YAML file as in the example files in the ```invoices``` directory.

Invoice styling and layout can be changed by editing ```templates/layout.yml``` and ```./templates/template.tex```

Invoices are created as PDF files using the glue script ```bin/generate_invoice.py```, which just merges the required YAML data into a single temporary file and passes that and the LaTeX template to ```pandoc```.

## Calculating GST

Inspect the scripts ```input_data/0?-*.sh``` to show how bank data is imported and filters successively added to ```bank.rules.csv``` as described in the [hledger manual](https://hledger.org/1.26/hledger.html#import-testing).

