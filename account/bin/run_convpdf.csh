#! /bin/bash -f

export PYTHONPATH=./pdfminer-20140328 
files=`ls pdfs`
echo $files
find pdfs -iname 'Ihre*' -print0 | while read -d $'\0' -r file;
do
    my=`echo $file | cut -d' ' -f7`
    my1=`echo $my | cut -d'-' -f1-2`
    echo "date $my1"
    echo "file $file"
    ./bin/pdfreader.py "$file" > txt/credit_${my1}.txt
done
find pdfs -iname 'Giro*' -print0 | while read -d $'\0' -r file;
do
    my=`echo $file | cut -d' ' -f6`
    my1=`echo $my | cut -d'-' -f1-2`
    echo "date $my1"
    echo "file $file"
    ./bin/pdfreader.py "$file" > txt/giro_${my1}.txt
done



