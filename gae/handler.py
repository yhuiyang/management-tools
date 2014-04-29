#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014, YH Yang <yhuiyang@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# python imports
import os
import logging

# GAE imports
import webapp2
from webapp2_extras import jinja2
from webapp2_extras.routes import RedirectRoute
from google.appengine.ext import ndb

# local imports


###################################################################################################
# model
###################################################################################################
AppDetailGroupKey = 'group-key'


class AppDetail(ndb.Model): # use google play game api project number as our model key string
    display_name = ndb.StringProperty(indexed=False)
    client_id = ndb.StringProperty(indexed=False)
    leaderboard_id = ndb.StringProperty(indexed=False)


####################################################################################################
# Request handlers
####################################################################################################
class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, template, **kwargs):
        # Renders a template and writes the result to the response.
        response_value = self.jinja2.render_template(template, **kwargs)
        self.response.write(response_value)


class ToolHandler(BaseHandler):

    def get(self):

        app_id = self.request.get('id', default_value=None)
        action = self.request.get('act', default_value=None)

        group_key = ndb.Key(AppDetail, AppDetailGroupKey)

        # execute specific function
        if app_id is not None and action is not None:
            # verify app_id and action
            detail = AppDetail.get_by_id(app_id, parent=group_key)
            if detail and action in ['hide', 'achievements', 'leaderboards']:
                list_all = False
                params = {
                    'APP_ID': app_id,
                    'LEADERBOARD_ID': detail.leaderboard_id,
                    'CLIENT_ID': detail.client_id,
                }
                if action == 'achievements':
                    template_file = 'achievements.html'
                elif action == 'hide':
                    template_file = 'hider.html'
                elif action == 'leaderboards':
                    template_file = 'scorer.html'
                self.render_response(template_file, **params)
                return

        # list all app
        app_details = AppDetail.query(ancestor=group_key)
        details = []
        for app_detail in app_details.iter():
            logging.info('app_detail: %s' % app_detail)
            detail = dict()
            detail['APP_ID'] = app_detail.key.string_id()
            detail['CLIENT_ID'] = app_detail.client_id
            detail['LEADERBOARD_ID'] = app_detail.leaderboard_id
            detail['DISPLAY_NAME'] = app_detail.display_name
            details.append(detail)

        params = {
            'details': details
        }
        self.render_response("home.html", **params)

    def post(self):

        # POST parameters: app_id, client_id, leaderboard_id, display_name
        group_key = ndb.Key(AppDetail, AppDetailGroupKey)
        detail = AppDetail(id=self.request.get('app_id'), parent=group_key)
        detail.client_id = self.request.get('client_id')
        detail.leaderboard_id = self.request.get('leaderboard_id')
        detail.display_name = self.request.get('display_name')
        detail.put()

        self.redirect_to('home')

    def put(self):
        # TODO:
        self.response.status = '501 Not Implemented'

    def delete(self):

        # DELETE parameter: id
        app_id = self.request.get('id', default_value=None)
        if app_id:
            group_key = ndb.Key(AppDetail, AppDetailGroupKey)
            detail_key = ndb.Key(AppDetail, app_id, parent=group_key)
            detail_key.delete()

        self.redirect_to('home')


##############################################################################################################
# app config
##############################################################################################################
config = {
    'webapp2_extras.jinja2': {
        'template_path': [
            'gae/templates',
            'tools',
            'tools/hide-o-matic',
            'tools/reset-o-matic',
            'tools/score-o-matic',
        ]
    }
}

##############################################################################################################
# app request route table
##############################################################################################################
routes = [
    RedirectRoute(r'/', handler=ToolHandler, name='home', strict_slash=True),
]

APP = webapp2.WSGIApplication(routes=routes, config=config, debug=os.environ.get('SERVER_SOFTWARE').startswith('Dev'))
