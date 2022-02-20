from email.policy import default
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
import datetime as dt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class MyUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(255))
    imgtype = db.Column(db.String(4))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at=db.Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)
    updated_at=db.Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)
    def __repr__(self):
        return self.img

class MyCube(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True) 
    front=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    back=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    right=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    left=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    ceiling=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    floor=db.Column(db.String(255),db.ForeignKey('my_upload.id'))
    created_at=db.Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    publish=db.Column(db.Boolean,nullable=False, default=False)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255),default="no description")

    def __repr__(self):
        return self.title



class MessageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    prediction = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.DateTime, index=True, default=datetime.now)
    
    def __repr__(self):
        return self.message



