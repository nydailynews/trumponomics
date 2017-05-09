#!/usr/bin/env python
# Ingest economic data
import sys
import argparse
import re
import string
import doctest
import json
from readwritesheet import EditSheet

class ApiInterface:

    def __init__():
        pass

def get_bls(series):
    """ Get data from the BLS.
        """
    pass

def main(args):
    """ main() only runs when this file's invoked from the command line, like so:
        $ python ingest.py labor-participation-rate monthly-job-creation
        """
    if args:
        sheet = EditSheet('Trumponomics Dashboard')
        sheet.set_options(args)
        for worksheet in args.sheets[0]:
            print worksheet
            sheet.worksheet = sheet.open_worksheet(worksheet)
            data = sheet.publish()
            f = open('www/_output/%s.json' % worksheet, 'wb')
            json.dump(data, f)
            f.close()


def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python ingest.py',
                                     description='Fetch data, update sheets',
                                     epilog='Example use: python ingest.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("sheets", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
