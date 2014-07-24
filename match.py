from google.appengine.ext import db
import player


class Match(db.Model):
    list_of_players = db.ListProperty(db.Key)

    def add_player_key(self, player_key):
        self.list_of_players.append(player_key)


def get_list_of_players(name):
    q = db.GqlQuery("SELECT list_of_players FROM Group WHERE name = '%s'" % name)
    return q




