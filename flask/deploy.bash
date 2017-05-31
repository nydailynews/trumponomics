#!/bin/bash
# ssh flat files to prod.
ENVIRON='PROD'
export environ=$ENVIRON
DEST=''
LOCATION_OVERRIDE=0
function html_only() { }

while [ "$1" != "" ]; do
    case $1 in
        -e | --environ ) shift
            ENVIRON=$1
            ;;
        -d | --dest ) shift
            DEST=$1
            ;;
        -h | --htmlonly ) shift
            function html_only() { find application/public \! -name "*.html" -type f -delete }
            ;;
        -f | --freeze ) shift
            python freeze.py; export environ='DEV'; exit 1
            ;;
    esac
    shift
done

# If we bailed on deploy mid-deploy we'll still have the public dir around.
if [ -d "application/public" ]; then rm -fr application/public; fi

html_only && \
python tests.py && \
    python freeze.py && \
    mv application/build application/public && \
    scp -r application/public $DEST && \
    mv application/public application/build
export environ='DEV'
