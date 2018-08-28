from app import db, app
from app.models.blacklist import Blacklist
from datetime import datetime, timedelta
import jwt


class Users(db.Model):
    """The class creates a user model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    user_username = db.Column(db.String(100), unique=True)
    user_password = db.Column(db.String(100))
    user_email = db.Column(db.String(200), unique=True)
    user_cats = db.relationship('Category',
                                order_by='Category.cat_id',
                                cascade='delete, all')

    def __init__(self, username, password, name=None, email=None):
        self.user_name = name
        self.user_username = username
        self.user_password = password
        self.user_email = email

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def generate_auth_token(self, expiration=60000):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=expiration),
                'iat': datetime.utcnow(),
                'sub': self.id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            return jwt_string
        except Exception as ex:
            raise Exception(ex)

    @staticmethod
    def check_not_blacklisted(token):
        """Check that the token is not in the blacklist table"""
        print()
        try:
            blacklist = Blacklist.query.filter_by(token=token).first()
            if blacklist is not None:
                if blacklist.token == token:
                    return False
            return True
        except:
            return False

    @staticmethod
    def decode_token(token):
        try:
            if Users.check_not_blacklisted(token):
                payload = jwt.decode(token, app.config['SECRET_KEY'])
                return payload['sub']
            else:
                raise ValueError('Invalid token')
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError()

    def __repr__(self):
        return '<Users %s>' % self.user_username

    # flask_login properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_username)
