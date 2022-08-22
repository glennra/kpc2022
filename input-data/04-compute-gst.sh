FILE=mycompany.journal

# see aggregate income and expenses
hledger -f $FILE --auto bal -2

# see GST collected and paid
hledger -f $FILE --auto bal -3
