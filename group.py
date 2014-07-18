from google.appengine.ext import db


class Group(db.Model):
    name = db.StringProperty(required=True)
    winner_bracket = db.BooleanProperty(required=True)
    list_of_players = db.ListProperty(required=True)


def add_player(group_name, player_name):
    q = db.GlQuery("SELECT * FROM Group WHERE name = '%s'" % player_name)
    g = q.get
    g.list_of_players.add(player_name)
    g.put()

def get_list_of_players(name):
     q = db.GlQuery("SELECT list_of_players FROM Group WHERE name = '%s'" % name)
     return q




