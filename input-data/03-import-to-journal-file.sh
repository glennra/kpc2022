rm -vf .latest*2021-04*.csv .latest*202104*.csv

FILE=mycompany.journal
rm -vf $FILE 
cat journal-header.dat >> $FILE

IMPORT="import"

# copy these for manual checking
hledger -f $FILE --rules-file=bank.csv.rules $IMPORT bank_2021-04-01_2021-09-30.csv
