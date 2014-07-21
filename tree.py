from google.appengine.ext import db
import group


class TournamentBrackets(db.Model):
    winner_bracket = db.ListProprty(default=[])
    loser_bracket = db.ListProprty(default=[])
