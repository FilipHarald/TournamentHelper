from google.appengine.ext import db
import player


class Group(db.Model):
    i = db.IntegerProperty(default=0)
    #list_of_players = db.ListProperty(default=[])

    def add_test_player(self, test):
        self.i = test
     #   self.list_of_players.__add__(test)


def add_player(group_name, player_name):
    q = db.GlQuery("SELECT * FROM Group WHERE name = '%s'" % group_name)
    g = q.get()
    g.list_of_players.add(player_name)
    g.put()


def get_list_of_players(name):
    q = db.GlQuery("SELECT list_of_players FROM Group WHERE name = '%s'" % name)
    return q




