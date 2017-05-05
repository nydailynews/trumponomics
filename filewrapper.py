#!/usr/bin/env python
# -*- coding: utf-8 -*-
# All-purpose file wrapper
import urllib2
import sys
import os.path
import types
 
class FileWrapper:
    """ class FileWrapper handles file write and download operations.
        """
    def __init__(self, filename):
        self.filename = filename
        self.fn = None
 
    def request(self, url, action='GET', headers={}, request_body=''):
    """ 
        """
        h = httplib2.Http('')
        response, content = h.request(url, action, headers=headers, body=request_body)
        if response.status > 299:
            print 'ERROR: HTTP response %s' % response.status
            sys.exit(1)
        return content
 
    def open(self):
        self.fn = open(self.filename, 'w')
 
    def close(self):
        self.fn.close
 
    def write(self, content):
    """ 
        """
        import string
        fn = open(self.filename, 'w')
        try:
            # Only run this on non-unicode strings
            if type(content) is not types.UnicodeType:
                content = content.decode('utf-8', 'replace')
        except (UnicodeError), e:
            # Figure out what the position of the error is
            import re
            regex = re.compile('.* position ([0-9]*):')
            r = regex.search(e.__str__())
            if len(r.groups()) > 0:
                position = int(r.groups()[0])
                str_range = [position - 10, position + 10]
            print e, content[str_range[0]:str_range[1]]
        fn.write(content.encode('utf-8', 'replace'))
        fn.close
 
    def read(self, filename=''):
    """ 
        """
        if filename == '':
            fn = open(self.filename, 'r')
        else:
            fn = open(filename, 'r')
        content = fn.read()
        fn.close
        return content
 
    def exists(self):
        return os.path.isfile(self.filename)
