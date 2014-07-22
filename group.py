from google.appengine.ext import db
import player


class Player(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    matches_won = db.IntegerProperty(default=0)


class Group(db.Model):
    name = db.StringProperty()
    list_of_players = db.ListProperty(default=[])

    def add_test_player(self, test):
        self.list_of_players.__add__(test)


def add_player(group_name, player_name):
    q = db.GlQuery("SELECT * FROM Group WHERE name = '%s'" % group_name)
    g = q.get()
    g.list_of_players.add(player_name)
    g.put()


def get_list_of_players(name):
    q = db.GlQuery("SELECT list_of_players FROM Group WHERE name = '%s'" % name)
    return q




