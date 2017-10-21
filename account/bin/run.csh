#! /bin/csh -f

echo "date,description,amount,category,account" > my.txt
./statement2csv.py -f txt/credit_07_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_08_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_09_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_10_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_11_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_12_16.txt -y 2016
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_01_17.txt -y 2016 -r 1
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_02_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_03_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_04_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_05_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_06_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_07_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_08_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
./statement2csv.py -f txt/credit_09_17.txt -y 2017
cat targo_cleaner.txt >> my.txt
