from app import db


class Blacklist(db.Model):
    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(200))
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, date):
        self.token = token
        self.date = date

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Blacklist %s>' % self.token
