from google.appengine.ext import db
import match


class TournamentBrackets(db.Model):
    winner_bracket = db.ListProperty(db.Key)
    loser_bracket = db.ListProperty(db.Key)
