#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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

import webapp2
import jinja2
import os
import cgi
from google.appengine.api import users
from google.appengine.ext import db
import player
import tournament_factory

#initializes templates (jinja)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def escape_html(s):
    return cgi.escape(s, quote=True)


class MainPage(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            self.render("main.html", nickname=nickname, logout_url=logout_url)
        else:
            sign_in_url = users.create_login_url('/')
            self.render("main.html", sign_in_url=sign_in_url)


class SignUpPage(Handler):
    def get(self):
        self.render('sign_up.html')

    def post(self):
        user = users.get_current_user()
        error_nick = "You need to enter your Starcraft 2 username"
        error_char_code = "You need to enter your Starcraft 2 character code"
        error_already_registered = "%s already has a Starcraft nickname connected to it" % user.nickname()
        nick = self.request.get("nick")
        char_code = self.request.get("char_code")
        if nick:
            error_nick = ""
            q = db.GqlQuery("SELECT * FROM Player WHERE user = :1", user)
            p = q.get()
            if not p:
                error_already_registered = ""
        if char_code:
            error_char_code = ""
        if error_nick or error_char_code or error_already_registered:
            self.render('sign_up.html',
                        nick=nick,
                        char_code=char_code,
                        error_nick=error_nick,
                        error_char_code=error_char_code,
                        error_already_registered=error_already_registered)
        else:
            player_to_be_added = player.Player(nick=nick, char_code=char_code)
            player_to_be_added.put()
            self.redirect('/playerhub')


class AdminPage(Handler):
    def get(self):
        user = users.get_current_user()
        nickname = user.nickname()
        if nickname:
            if nickname == 'Filip.Harald' or nickname == 'limstift_@hotmail.com' or nickname == 'eskil.petersson':
                self.render('admin.html')
            else:
                self.redirect('/')


class ListOfPLayersPage(Handler):
    def get(self):
        players = db.GqlQuery('select * from Player')
        self.render('list_of_players.html', players=players)


class ProjectorViewPage(Handler):
    def get(self):
        self.render('projector_view.html')


class TestPage1(Handler):
    def get(self):
        tournament_factory.run_test1()


class TestPage2(Handler):
    def get(self):
        tournament_factory.set_groups()
        players = db.GqlQuery('select * from Player')
        self.render('list_of_players.html', players=players)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', SignUpPage),
                               ('/admin', AdminPage),
                               ('/playerhub', ListOfPLayersPage),
                               ('/admin/projectorview', ProjectorViewPage),
                               ('/test1', TestPage1),
                               ('/test2', TestPage2)],
                              debug=True)
