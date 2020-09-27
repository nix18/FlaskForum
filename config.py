import os
import pymysql

DB_URI = 'mysql+pymysql://root:yourpassword@localhost:3306/mybbs?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

SECRET_KEY = os.urandom(24)

db = pymysql.connect("127.0.0.1", "root", "yourpassword", "mybbs")
cur = db.cursor()

def searchtz(q):
    DH_uri = "call searchtz('%s')"%(q)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchall()
    result = []
    for i in geter:
        result.append(i[0])
    print(result)
    return result

def searchlimit(tel):
    DH_uri = "select tel2limit('%s')"%(tel)
    cur.execute(DH_uri)
    cur.connection.commit()
    getlimit = cur.fetchone()
    return getlimit[0]

def searchtzlimit(id):
    DH_uri = "select tzid2limit('%s')"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def tzidtoblock(id):
    DH_uri = "select tzid2block('%s')"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def dhtoid(dh):
    DH_uri = "select dh2id('%s')" % (dh)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def plcount(id):
    DH_uri = "select tzcountpl('%s')"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def bkcount():
    DH_uri = "select countbk()"
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def indexrows(bks):
    rowcount = 0
    while bks/3 > 0:
        rowcount += 1
        bks = bks - 3
    return rowcount

def tzcount():
    DH_uri = "select bkcounttz()"
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def bkplcount(id):
    DH_uri = "select countpl('%s')"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def plup(id):
    DH_uri = "update pinglun set pinglunup=pinglunup+1 where id='%s'"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    return 1

def pldown(id):
    DH_uri = "update pinglun set pinglundown=pinglundown+1 where id='%s'"%(id)
    cur.execute(DH_uri)
    cur.connection.commit()
    return 1

def bkname2id(name):
    DH_uri = "select bkurlsearchbid('%s')" % (name)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def bkid2name(id):
    DH_uri = "select bkid2name('%s')" % (id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def plid2tzid(id):
    DH_uri = "select plid2zhutieid('%s')" % (id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]


def tieziup(id):
    DH_uri = "update zhutie set zhutieup=zhutieup+1 where zhutieid='%s'" % (id)
    cur.execute(DH_uri)
    cur.connection.commit()
    return 1

def tel2pw(tel):
    DH_uri = "select tel2pw('%s')" % (tel)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]

def tzid2userid(id):
    DH_uri = "select tzid2userid('%s')" % (id)
    cur.execute(DH_uri)
    cur.connection.commit()
    geter = cur.fetchone()
    return geter[0]