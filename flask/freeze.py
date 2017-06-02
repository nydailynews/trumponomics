#!/usr/bin/env python
# More here: http://pythonhosted.org/Frozen-Flask/
from datetime import date, timedelta
import argparse
import sys
import os
import doctest
from string import replace
from flask_frozen import Freezer
from application import app, pages
app.debug = False

environ = os.getenv('environ', 'DEV')
if environ == 'PROD':
    app.url_root = '/project/trumponomics/'

class FreezeThings:
    """ We put the Flask Frozen methods in this class so we don't have to
        freeze everything at once.
        >>> f = FreezeThings()
        >>> files_frozen = f.freezer.freeze()
        """

    def __init__(self):
        """
            >>> f = FreezeThings()
            """
        self.freezer = Freezer(app)
        self.details_all = []

    def freeze_urls(self, path):
        """ Freeze one url (if passed a path) or a handful (if passed a list
            of paths).
            >>> f = FreezeThings()
            >>> f.freeze_urls('/detail/gdp-growth/')
            """
        @self.freezer.register_generator
        def freeze_urls():
            return path

    def do_detail(self):
        """ The methods that freeze everything in /detail/ and below.
            >>> f = FreezeThings()
            >>> f.do_detail()
            """

        @self.freezer.register_generator
        def detail():
            for item in self.details_all:
                yield {'detail': item}

def main(args):
    """ What we run when we run this from the command line.
        >>> main(build_parser(None))
        """
    f = FreezeThings()

    if args.paths[0]:
        f.freeze_urls(args.paths[0])
        f.freezer.freeze()
        return True

    f.freezer.freeze()

def build_parser(args):
    """ A method to handle argparse.
        >>> args = build_parser(None)
        >>> # args = Namespace(archiveonly=False, json=False, location=False, paths=[[]], verbose=True)
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python freeze.py',
                                     description='''Turn the flask app into a
                                                    bunch of html files.''',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument(dest="paths", action="append", nargs="*")
    return parser.parse_args()

if __name__ == '__main__':
    args = build_parser(sys.argv)
    if args.verbose == True:
        doctest.testmod(verbose=True)
    main(args)
