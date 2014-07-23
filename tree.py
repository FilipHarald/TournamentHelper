from google.appengine.ext import db
import group


class TournamentBrackets(db.Model):
    winner_bracket = db.ListProperty(int, default=None)
    loser_bracket = db.ListProperty(int, default=None)
