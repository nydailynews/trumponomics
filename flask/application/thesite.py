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
# PRIMARY VIEWS
# =========================================================


def get_lead_item(tabs):
    """ Return the index of an item for placement in the lead slot on the index.
        """
    candidates = tabs['top']
    count = len(candidates)
    daynum = datetime.today().weekday()
    return daynum % count

@app.route('/')
def index():
    app.page['title'] = 'Trumponomics: Measuring the U.S. economic statistics of Donald Trump\'s presidency'
    app.page['description'] = ''
    app.page['url'] = build_url(app, request)

    tabs = {
        'all': ['base-unemployment','monthly-job-creation','labor-participation-rate','year-over-year-wage-growth','gdp-growth','african-american-unemployment','manufacturing-jobs','coal-mining-jobs','uninsured-rate','us-trade-deficit','interior-removals','total-outstanding-debt','americans-on-food-stamps'],
        'top': ['base-unemployment','monthly-job-creation','labor-participation-rate','year-over-year-wage-growth','gdp-growth'],
        'used': []
    }
    lead_index = get_lead_item(tabs)
    lead = tabs['all'][lead_index]
    tabs['all'].remove(lead)
    items = tabs['all']

    data_raw = json.load(filters.json_check('_output/index.json'))
    data = {}
    for item in data_raw:
        data[item['slug']] = item

    response = {
        'app': app,
        'lead': lead,
        'indicators': items,
        'data': data,
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
    data = json.load(filters.json_check('_output/%s.json' % detail))
    response = {
        'app': app,
        'page': app.page,
        'data': data
    }
    return render_template('detail.html', response=response)

# =========================================================
# === NOT DEPLOYED YET === #
# =========================================================

