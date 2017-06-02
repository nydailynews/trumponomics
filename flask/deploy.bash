#!/bin/bash
# ssh flat files to prod.
ENVIRON='PROD'
export environ=$ENVIRON
SERVER='qa'
DIR='/apps/project/'
PROJECT='trumponomics'
LOCATION_OVERRIDE=0
html_only() { 
    echo ''
}

while [ "$1" != "" ]; do
    case $1 in
        -e | --environ ) shift
            ENVIRON=$1
            ;;
        -p | --project ) shift
            PROJECT=$1
            ;;
        -s | --server ) shift
            SERVER=$1
            ;;
        -d | --dir ) shift
            DIR=$1
            ;;
        -h | --htmlonly ) shift
            html_only() {
                find application/public \! -name "*.html" -type f -delete;
            }
            ;;
        -f | --freeze ) shift
            python freeze.py; export environ='DEV'; exit 1
            ;;
    esac
    shift
done

# If we bailed on deploy mid-deploy we'll still have the public dir around.
if [ -d "application/$PROJECT" ]; then rm -fr application/$PROJECT; fi

#python tests.py && \
html_only && \
    python freeze.py && \
    mv application/build application/$PROJECT && \
    scp -r application/$PROJECT $SERVER:$DIR && \
    mv application/$PROJECT application/build

export environ='DEV'
