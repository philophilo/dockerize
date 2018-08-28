from app import db
from app.models.category import Category
from datetime import datetime


class Recipes(db.Model):
    """The class creates a recipes model"""
    __tablename__ = 'recipes'
    rec_id = db.Column(db.Integer, primary_key=True)
    rec_name = db.Column(db.String(100), nullable=False, unique=True)
    rec_cat = db.Column(db.Integer, db.ForeignKey(Category.cat_id))
    rec_ingredients = db.Column(db.String(500), nullable=False)
    rec_description = db.Column(db.String(200), nullable=True)
    rec_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, category, ingredients, description=None):
        self.rec_name = name
        self.rec_cat = category
        self.rec_date = datetime.now()
        self.rec_ingredients = ingredients
        self.rec_description = description

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
        return '<Recipes %s>' % self.rec_name
