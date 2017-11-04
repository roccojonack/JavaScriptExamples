#! /bin/bash -f

echo "date,description,amount,category,account" > my.txt
./bin/statement2csv.py -f txt/credit_2016-07.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2016-08.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2016-09.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2016-10.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2016-11.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2016-12.txt -y 2016
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-01.txt -y 2016 -r 1
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-02.txt -y 2017 -r 0
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-03.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-04.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-05.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-06.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-07.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-08.txt -y 2017
cat targo_cleaner.txt >> my.txt
./bin/statement2csv.py -f txt/credit_2017-09.txt -y 2017
cat targo_cleaner.txt >> my.txt
