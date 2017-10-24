#! /bin/csh -f

foreach x (ls pdfs/Ihre*)
#    set words = `echo $x:q | sed 's/ / /g'`
    set  my = `echo $x | cut -d' ' -f7`
    set  my1 = `echo $my | cut -d'-' -f0-2`
   
    echo "date my $my1"
    echo "file $x"
    ./bin/pdfreader.py "$x" > txt/credit_${my1}.txt
end


