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


#initializes templates (jinja)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Player(db.Model):
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    match_won = db.IntegerProperty()


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
        #self.response.headers['Content-Type'] = 'text/html'
        visits = self.request.cookies.get('visits', '0')
        if visits.isdigit():
            visits = int(visits) + 1
        else:
            visits = 0
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            self.render("main.html", visits=visits, nickname=nickname, logout_url=logout_url)
            #greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
            #            (user.nickname(), users.create_logout_url('/')))
        else:
            sign_in_url = users.create_login_url('/')
            self.render("main.html", visits=visits, sign_in_url=sign_in_url)
            #greeting = ('<a href="%s">Sign in or register</a>.' %
            #            users.create_login_url('/'))


class SignUpPage(Handler):
    def get(self):
        self.render('signup.html')

    def post(self):
        error_nick = "You need to enter your Starcraft 2 username"
        error_char_code = "You need to enter your Starcraft 2 character code"
        nick = self.request.get("nick")
        char_code = self.request.get("char_code")
        if nick:
            error_nick = ""
        if char_code:
            error_char_code = ""
        if error_nick or error_char_code:
            self.render('main.html',
                        nick=nick,
                        char_code=char_code,
                        error_nick=error_nick,
                        error_char_code=error_char_code)
        else:
            player = Player(nick=nick, char_code=char_code)
            player.put()
            return webapp2.redirect('list_of_players.html')

class AdminPage(Handler):
    def get(self):
        self.render('admin_login.html')



class ListOfPLayersPage(Handler):
    def get(self):
        self.render('list_of_players.html')


class ProjectorViewPage(Handler):
    def get(self):
        self.render('projector_view.html')




app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', SignUpPage),
                               ('/admin', AdminPage),
                               ('/playerhub', ListOfPLayersPage),
                               ('/admin/projectorview', ProjectorViewPage)],
                              debug=True)
