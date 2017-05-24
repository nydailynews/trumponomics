#!/usr/bin/env python
from flask import g, render_template, url_for, redirect, abort, request
from datetime import datetime, date, timedelta
from collections import OrderedDict
import inspect
import os
import json
import string
from application import app
import filters
from werkzeug.contrib.atom import AtomFeed


datetimeformat = '%Y-%m-%d %H:%M:%S'

def build_url(app, request):
    """ Return a URL for the current view.
        """
    return '%s%s' % (app.url_root, request.path[1:])

# =========================================================
# HOMEPAGE VIEW
# =========================================================

@app.route('/')
def index():
    app.page['title'] = ''
    app.page['description'] = ''
    app.page['url'] = build_url(app, request)

    response = {
        'app': app
    }
    return render_template('home.html', response=response)

# =========================================================
# === NOT DEPLOYED YET === #
# =========================================================

