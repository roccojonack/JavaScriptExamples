#! /bin/bash -f

if [ $# == 0 ]; then
    echo "No args, using 8888 as default port number"
    port=8888
else
    echo "will use $argv[1] as port number"
    port=$1
fi

python -m SimpleHTTPServer $port
