from app import db
from app.models.users import Users
from datetime import datetime


class Category(db.Model):
    """The class creates a category model"""
    __tablename__ = 'category'
    cat_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    cat_name = db.Column(db.String(100), nullable=False, unique=True)
    cat_description = db.Column(db.String(200), nullable=True)
    cat_date = db.Column(db.DateTime, nullable=False)
    cat_recipes = db.relationship('Recipes',
                                  order_by='Recipes.rec_id',
                                  cascade='delete, all')

    def __init__(self, cat_name, user_id, description=None):
        self.cat_name = cat_name
        self.user_id = user_id
        self.cat_description = description
        self.cat_date = datetime.now()

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
        return '<Category: %s>' % self.cat_name
