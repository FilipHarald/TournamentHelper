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
        error_wrong_pay_code = "Your code was not valid"
        error_pay_code = "You need to enter your pay code"
        nick = self.request.get("nick")
        char_code = self.request.get("char_code")
        pay_code = self.request.get("pay_code")
        if nick:
            error_nick = ""
            q = db.GqlQuery("SELECT * FROM Player WHERE user = :1", user)
            p = q.get()
            if not p:
                error_already_registered = ""
        if char_code:
            error_char_code = ""
        if pay_code:
            error_pay_code = ""
            q = db.GqlQuery("Select * FROM Paycode WHERE pay_code = '%s'" % pay_code)
            temp = q.get()
            if temp:
                db.delete(temp.key())
                error_wrong_pay_code = ""
        else:
            error_wrong_pay_code = ""
        if error_nick or error_char_code or error_already_registered or error_pay_code or error_wrong_pay_code:
            self.render('sign_up.html',
                        nick=nick,
                        char_code=char_code,
                        error_nick=error_nick,
                        error_char_code=error_char_code,
                        error_already_registered=error_already_registered,
                        error_pay_code=error_pay_code,
                        error_wrong_pay_code=error_wrong_pay_code)
        else:
            player_to_be_added = player.Player(nick=nick, char_code=char_code)
            player_to_be_added.put()
            self.redirect('/playerhub')


class AdminPage(Handler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            if nickname:
                if nickname == 'Filip.Harald' or nickname == 'limstift_@hotmail.com' or nickname == 'eskil.petersson':
                    self.render('admin.html')
                else:
                    self.redirect('/')
        else:
                    self.redirect('/')



class ListOfPLayersPage(Handler):
    def get(self):
        players = db.GqlQuery('select * from Player')
        self.render('list_of_players.html', players=players)


class ProjectorViewPage(Handler):
    def get(self):
        q = db.GqlQuery("Select * FROM TournamentBrackets")
        t_b = q.get()
        if t_b:
            winner_bracket_keys = t_b.winner_bracket
            winner_bracket_players = []
            for k in winner_bracket_keys:
                if k:
                    winner_bracket_players.append(db.get(k))
                else:
                    winner_bracket_players.append(k)
            loser_bracket_keys = t_b.loser_bracket
            loser_bracket_players = []
            for k in loser_bracket_keys:
                if k:
                    loser_bracket_players.append(db.get(k))
                else:
                    loser_bracket_players.append(k)
            self.render('projector_view.html', winner_bracket=winner_bracket_players, loser_bracket=loser_bracket_players)


    def post(self):
        nick_n_char_code = self.request.get("nick_n_char_code")
        q = db.GqlQuery("Select * FROM TournamentBrackets")
        t_b = q.get()
        if nick_n_char_code and t_b:
            nick, char_code = nick_n_char_code.split('.')
            winner_bracket_keys = t_b.winner_bracket
            loser_bracket_keys = t_b.loser_bracket
            count = 0
            fixed = False
            for p in winner_bracket_keys:
                if p:
                    player = db.get(p)
                    if nick is player.nick:
                        if char_code is player.char_code:
                            t_b.winner_bracket[count-1/2] = player.key()
                            fixed = True
                            break
                count += 1
            if not fixed:
                count = 0
                for p in loser_bracket_keys:
                    if p:
                        player = db.get(p)
                        if nick is player.nick:
                            if char_code is player.char_code:
                                t_b.loser_bracket[count-1/2] = player.key()
                                break
                    count += 1
            t_b.put()
        self.redirect('/admin/projectorview')


class GroupViewPage(Handler):
    def get(self):
        list_of_players = db.GqlQuery("SELECT * FROM Player ORDER BY group_nbr ASC , matches_won DESC")
        self.render('group_view.html', list_of_players=list_of_players)


    def post(self):
        nick_n_char_code = self.request.get("nick_n_char_code")
        if nick_n_char_code:
            nick, char_code = nick_n_char_code.split('.')
            q = db.GqlQuery("Select * FROM Player WHERE nick= '%s' AND char_code='%s'" % (nick, char_code))
            p = q.get()
            p.add_match_won()
            p.put()
        self.redirect('/admin/groupview')


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
                               ('/admin/groupview', GroupViewPage),
                               ('/test1', TestPage1),
                               ('/test2', TestPage2)],
                              debug=True)
