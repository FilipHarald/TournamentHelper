from google.appengine.ext import db


class Player(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    nick = db.StringProperty(required=True)
    char_code = db.StringProperty(required=True)
    group_nbr = db.IntegerProperty(default=0)
    matches_won = db.IntegerProperty(default=0)

    def set_group_nbr(self, nbr):
        self.group_nbr = nbr


def get_all_players():
    q = db.GqlQuery("SELECT * FROM Player")
    return q.run()


def get_matches_won(user):
    q = db.GqlQuery("SELECT matches_won FROM Player WHERE user = '%s'" % user)
    m = q.get()
    return m


def add_match_won(user):
    q = db.GqlQuery("SELECT * FROM Player WHERE user = '%s'" % user)
    u = q.get()
    u.matches_won += 1
    u.put()


def reset_matches_won(user):
    q = db.GqlQuery("SELECT * FROM Player WHERE user = '%s'" % user)
    u = q.get()
    u.matches_won = 0
    u.put()


