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
from app_config import details


datetimeformat = '%Y-%m-%d %H:%M:%S'

def build_url(app, request):
    """ Return a URL for the current view.
        """
    return '%s%s' % (app.url_root, request.path[1:])

def build_keywords_array(value):
    """Take a comma-separated string of items and turn it into an array.
        """
    pass

# =========================================================
# HOMEPAGE VIEW
# =========================================================

@app.route('/')
def index():
    app.page['title'] = 'Trumponomics: Measuring certain U.S. economic statistics of Donald Trump\'s presidency'
    app.page['description'] = ''
    app.page['url'] = build_url(app, request)

    response = {
        'app': app
    }
    return render_template('index.html', response=response)

@app.route('/detail/')
def detail_index():
    return redirect(url_for('index'))

@app.route('/detail/<detail>/')
def detail(detail):
    d = details[detail]
    
    app.page['title'] = d['title']
    if d['title'] == '':
        app.page['title'] = detail.replace('-', ' ').title()
    app.page['description'] = d['description']
    app.page['url'] = build_url(app, request)

    context = {}
    data = filters.json_check('_output/%s.json' % detail)
    response = {
        'app': app,
        'page': app.page,
        'data': data
    }
    return render_template('detail.html', response=response)

# =========================================================
# === NOT DEPLOYED YET === #
# =========================================================

