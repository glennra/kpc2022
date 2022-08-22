
FILE=mycompany.journal

hledger -f $FILE --auto print -O csv > mycompany.csv

../bin/csv_to_myob.py mycompany.csv
