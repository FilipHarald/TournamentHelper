from google.appengine.ext import db


class Paycode(db.Model):
    pay_code = db.StringProperty(required = True)