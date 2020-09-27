from datetime import datetime

from exts import db

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    registerTime = db.Column(db.DATE, nullable=False)
    userlimit = db.Column(db.Integer, nullable=False, default=1)
    email = db.Column(db.String(50), nullable=False)
    touxiang = db.Column(db.Integer, nullable=False, default=0)

class bankuai(db.Model):
    __tablename__ = 'block'
    blockid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blockname = db.Column(db.String(50), nullable=False)
    urlfor = db.Column(db.String(255), nullable=False)
    urlfor1 = db.Column(db.String(255), nullable=False)
    plscount = db.Column(db.Integer, nullable=False, default=0)
    tzscount = db.Column(db.Integer, nullable=False, default=0)

class tiezi(db.Model):
    __tablename__ = 'zhutie'
    zhutieid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zhutietitle = db.Column(db.String(200), nullable=False)
    zhutievalue = db.Column(db.String(500), nullable=False)
    zhutielimit = db.Column(db.Integer, nullable=False, default=1)
    zhutieup = db.Column(db.Integer, nullable=False, default=0)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'))
    blockid = db.Column(db.Integer, db.ForeignKey('block.blockid', ondelete='CASCADE'))
    zhutieTime = db.Column(db.DATE, nullable=False)
    author = db.relationship('User', backref=db.backref('tiezis', cascade='all, delete-orphan', passive_deletes=True))

class pinglun(db.Model):
    __tablename__ = 'pinglun'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    pinglunup = db.Column(db.Integer, nullable=False, default=0)
    pinglundown = db.Column(db.Integer, nullable=False, default=0)
    pingluntime = db.Column(db.DATE, nullable=False, default=datetime.now())
    zhutieid = db.Column(db.Integer, db.ForeignKey('zhutie.zhutieid', ondelete='CASCADE'))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid', ondelete='CASCADE'))
    zhutie = db.relationship('tiezi', backref=db.backref('pls', order_by=pingluntime.desc(), cascade='all, delete-orphan', passive_deletes=True))
    author = db.relationship('User', backref=db.backref('pls', cascade='all, delete-orphan', passive_deletes=True))
