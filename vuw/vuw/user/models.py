# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from vuw.database import Column, PkModel, db, reference_col, relationship
from vuw.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

class Upload(PkModel):
    id=Column(db.Integer, primary_key=True)
    img=Column(db.String(255))
    imgtype=Column(db.String(4))
    user_id=Column(db.Integer,db.ForeignKey('users.id'))##########
    created_at=Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)
    updated_at=Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)

    def __repr__(self): # raw representation of string
        return self.img

class Cube(PkModel):
    id=Column(db.Integer, primary_key=True) 
    front=Column(db.String(255),db.ForeignKey('upload.img'))##########
    back=Column(db.String(255),db.ForeignKey('upload.img'))##########
    right=Column(db.String(255),db.ForeignKey('upload.img'))##########
    left=Column(db.String(255),db.ForeignKey('upload.img'))##########
    top=Column(db.String(255),db.ForeignKey('upload.img'))##########
    bottom=Column(db.String(255),db.ForeignKey('upload.img'))##########
    imgtype=Column(db.String(4))
    created_at=Column(db.DateTime,nullable=False,index=True, default=dt.datetime.utcnow)
    user_id=Column(db.Integer,db.ForeignKey('users.id'))#####
    publish=Column(db.Boolean,nullable=False, default=False)
    output_img=Column(db.String(255))

    def __repr__(self):
        return self.output_img



