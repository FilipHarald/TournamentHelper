from google.appengine.ext import db

class Player(db.Model):
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    match_won = db.IntegerProperty()
