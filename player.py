from google.appengine.ext import db


class Player(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    matches_won = db.IntegerProperty(required=True,default=0)

#returns null if user not found


def get_matches_won(user):
    q = db.GlQuery("SELECT matches_won FROM Player WHERE user = '%s'" % user)
    m = q.get()
    return m


def add_match_won(user):
    q = db.GlQuery("SELECT * FROM Player WHERE user = '%s'" % user)
    u = q.get()
    u.matches_won += 1
    u.put()


def reset_matches_won(user):
    q = db.GlQuery("SELECT * FROM Player WHERE user = '%s'" % user)
    u = q.get()
    u.matches_won = 0
    u.put()


