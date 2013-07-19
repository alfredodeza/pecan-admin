import os
from hashlib import sha1
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String, Unicode
from sqlalchemy.orm import synonym, relationship
from sqlalchemy.orm.exc import DetachedInstanceError
from pecan_admin.models import Base


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    username = Column(String(64), unique=True)
    _password = Column('password', Unicode(80))
    email = Column(String(64))
    signup_date = Column(DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.signup_date = datetime.utcnow()
        self._set_password(password)

    def __repr__(self):
        try:
            return '<User %r>' % self.username
        except DetachedInstanceError:
            return '<User detached>'

    def _set_password(self, password):
        """Hash password on the fly."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hased password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # fields
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the password hashed"""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool
        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()
