from google.appengine.ext import db


class TournamentBrackets(db.Model):
    winner_bracket = db.ListProperty(db.Key)
    loser_bracket = db.ListProperty(db.Key)
