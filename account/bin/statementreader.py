#! /usr/bin/python
import re
from optparse import OptionParser
import datetime

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
(options, args)  = parser.parse_args()
file_name_input  = options.filename
file_name_output = 'tmp.txt'
print "Handling file input ", file_name_input
f    = open(file_name_input, "r")
fout = open(file_name_output, "w")
data = f.readlines()
legendHeader  = "date;description;amount;category;account\n"
fout.write(legendHeader)
for line in data:
    newWord = line.replace(',',';')
    fout.write(newWord)

    
