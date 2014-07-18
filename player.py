from google.appengine.ext import db


class Player(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    match_won = db.IntegerProperty()