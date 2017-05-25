#!/usr/bin/env python
# Read, write and publish the spreadsheets
import sys
import argparse
import re
import string
import doctest
import json
from sheetmodule.writesheet import Sheet

class EditSheet(Sheet):

    def update(self, worksheet=None):
        """ Publish the data in whatever permutations we need.
            This assumes the spreadsheet's key names are in the first row.
            >>> sheet = Sheet('test-sheet', 'worksheet-name')
            >>> sheet.fix()
            True
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        i = 0
        for row in cell_list:
            i += 1
            print row
            if row[0] == '':
                value = url.replace('/', '-')
                column = 1
                worksheet.update_cell(i, column, value)

        return True

    def publish(self, worksheet=None):
        """ Print out the json we'll use in different lists.
            """
        if not self.sheet or worksheet:
            self.sheet = self.open_worksheet(worksheet)

        if not worksheet:
            worksheet = self.worksheet

        cell_list = worksheet.get_all_values()
        recent = []
        for i, row in enumerate(cell_list):
            i += 1
            if i == 1:
                keys = row
                continue

            r = dict(zip(keys, row))

            if hasattr(r, 'value') and r['value'] == '':
                continue

            recent.append(r)

        return recent

def main(args):
    """ main() only runs when this file's invoked from the command line, like so:
        $ python readwritesheet.py labor-participation-rate monthly-job-creation
        """
    if args:
        sheet = EditSheet('Trumponomics Dashboard')
        sheet.set_options(args)
        basedir = '%s/_output/' % args.basedir
        for worksheet in args.sheets[0]:
            dest = '%s%s.json' % (basedir, worksheet)
            if args.verbose:
                print "Writing %s to %s" % (worksheet, dest)
            sheet.worksheet = sheet.open_worksheet(worksheet)
            data = sheet.publish()
            f = open(dest, 'wb')
            json.dump(data, f)
            f.close()


def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python readwritesheet.py',
                                     description='Log in to Google sheets and do stuff with a spreadsheet and its tabs.',
                                     epilog='Example use: python readwritesheet.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("-b", "--basedir", dest="basedir", default='flask')
    parser.add_argument("sheets", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
