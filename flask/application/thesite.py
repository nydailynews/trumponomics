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
        'all': ['base-unemployment','monthly-job-growth','labor-participation-rate','year-over-year-wage-growth','gdp-growth','african-american-unemployment','manufacturing-jobs','coal-mining-jobs','uninsured-rate','us-trade-deficit','interior-removals','total-outstanding-debt','americans-on-food-stamps'],
        'top': ['base-unemployment','monthly-job-growth','labor-participation-rate','year-over-year-wage-growth','gdp-growth'],
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

class DetailView(object):
    """ DetailView abstracts common detail requests.
        """

    def __init__(self, detail):
        """ Do most of the legwork on the view, construct the response dict.
            """
        self.detail = detail
        d = details[detail]
        
        app.page['title'] = d['title']
        if d['title'] == '':
            app.page['title'] = detail.replace('-', ' ').title()
        app.page['description'] = d['description']
        app.page['url'] = build_url(app, request)

        context = {}
        data = json.load(filters.json_check('_output/%s.json' % detail))
        index = json.load(filters.json_check('_output/index.json'))
        self.response = {
            'app': app,
            'page': app.page,
            'index': self._get_index_item(index, detail),
            'data': data,
            'latest': self._get_latest_data(data)
        }

    def _get_unit_of_time(self, dict_):
        """ Is this a daily / weekly / monthly or quarterly number?
            Returns a string.
            """
        units = ['quarter', 'month', 'week', 'day']
        for item in units:
            if item in dict_:
                return item

    def _get_latest_data(self, data):
        """ Get the latest item that has an actual value in the data object.
            """
        prev = {}
        prev_prev = {}
        for item in data:
            if item['value'] == '':
                prev['previous_value'] = prev_prev['value']
                prev['unit_of_time'] = self._get_unit_of_time(item)
                return prev
            prev_prev = prev
            prev = item

    def _get_index_item(self, index, slug):
        """ Look through the index object for the record that has a slug "slug".
            """
        for item in index:
            if item['slug'] == slug:
                return item

    def generic(self):
        return render_template('detail.html', response=self.response)

    def specific(self):
        return render_template('detail-%s.html' % self.detail, response=self.response)

@app.route('/detail/<any("monthly-job-growth"):detail>/')
def detail_specific(detail=''):
    view = DetailView(detail)
    return view.specific()

@app.route('/detail/<detail>/')
def detail(detail):
    print 'b'
    view = DetailView(detail)
    return view.generic()
