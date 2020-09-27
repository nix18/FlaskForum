from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, session
from decorators import login_limit
import config
from models import User, tiezi, pinglun, bankuai
from exts import db
from sqlalchemy import or_
import os
from flask import Flask, request, redirect, url_for

UPLOAD_FOLDER = os.getcwd()+'\\static\\images'

app = Flask(__name__)
app.config.from_object(config)
app.config['SECRET_KEY'] = "python"
db.init_app(app)

global zancontrol
zancontrol=0
global caicontrol
caicontrol=0


@app.route('/')
def index():
    usertel = session.get('usertel')
    id = config.dhtoid(usertel)
    bks = config.bkcount()
    rowcount = config.indexrows(bks)
    i = 3
    a = []
    b = []
    bid = 1

    while rowcount > 0:
        while i > 0:
            bk = bankuai.query.filter(bankuai.blockid == bid).first()
            if bk == None:
                a.append(' ')
            else:
                a.append(bk)
            bid += 1
            i -= 1
        b.append(a)
        a = []
        rowcount -= 1
        i = 3
    blocks = bankuai.query.all()
    return render_template('index.html', userid=id, b=b, blocks=blocks)

@app.route('/login/',methods=['GET', 'POST'])
def login():
    blocks = bankuai.query.all()


    if request.method == 'GET':
         return render_template('login.html', blocks=blocks, pws=0)
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        userpw = config.tel2pw(telephone)

        if len(telephone) == 0 | len(password) == 0:
            return redirect(url_for('login'))
        if password != userpw:
            return render_template('login.html', blocks=blocks, pws=1)
        user = User.query.filter(User.tel == telephone, User.password == password).first()
        if user:
            session["usertel"] = user.tel
            session.permanent = True
            print(session.get("usertel"))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', blocks=blocks, pws=1)

@app.route('/regist/',methods=['GET', 'POST'])
def regist():
    blocks = bankuai.query.all()
    if request.method == 'GET':
        return render_template('regist.html', blocks=blocks,pw0=0)
    else:
        telephone = request.form.get('telephone')
        username  = request.form.get('username')
        password0 = request.form.get('password0')
        password1 = request.form.get('password1')
        gender    = request.form.get('gender')
        age       = request.form.get('age')
        email     = request.form.get('e-mail')
        if len(telephone) == 0 or len(username) == 0 or len(password0) == 0 or len(password1) == 0 or len(gender) == 0 or len(age) == 0 or len(email) == 0:
            return redirect(url_for("regist"))

    #检测手机号码有没有被注册


        user = User.query.filter(User.tel == telephone).first()
        if user:
            return render_template('regist.html', blocks=blocks,pw0=1)

        else:
            if password0 != password1:
                return redirect(url_for("regist"))
            else:
                time = "2019-11-9"
                user = User(tel=telephone, username=username, password=password0, gender=gender, age=age, email=email, registerTime=time)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/forum/<blockname>/<pid>', methods=['GET', 'POST'])
@login_limit
def forum(blockname, pid):
    block = bankuai.query.filter(bankuai.urlfor1 == blockname).first()
    bkid = config.bkname2id(blockname)
    blocks = bankuai.query.all()
    tie = tiezi.query.filter(tiezi.blockid == bkid).order_by(tiezi.zhutieTime.desc()).all()
    i = int(pid)
    zpid = int(len(tie) / 5 + 1)
    zpids = []
    while zpid != 0:
        zpids.append(zpid)
        zpid = zpid - 1
    zpids = sorted(zpids)
    k = 5 * (i - 1)
    j = 5 * i
    return render_template('bankauibase.html', fatie=tie[k:j], zpids=zpids, blocks=blocks, block=block)


@app.route('/fatie/', methods=['GET', 'POST'])
@login_limit
def fatie():
    blocks = bankuai.query.all()
    if request.method == 'GET':

        return render_template('fatie.html', blocks=blocks)
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        blockid = request.form.get('blockid')
        zhutielimit = request.form.get('zhutielimit')
        usertel = session.get("usertel")
        if len(title) == 0 or len(content) == 0:
            return redirect(url_for('fatie'))
        else:
            user = User.query.filter(User.tel == usertel).first()
            userid = user.userid
            zhutie = tiezi(zhutietitle=title, zhutievalue=content, zhutielimit=zhutielimit, blockid=blockid, userid=userid)
            zhutie.author = user
            db.session.add(zhutie)
            db.session.commit()
            return redirect(url_for('index'))

@app.route('/addblock/', methods=['GET', 'POST'])
@login_limit
def addblock():
    blocks = bankuai.query.all()
    usertel = session.get('usertel')
    userlimit = config.searchlimit(usertel)
    if userlimit < 5:
        return render_template('LimitNone.html', blocks=blocks)
    if request.method == 'GET':
        return render_template('addblock.html', blocks=blocks)
    else:
        blockname = request.form.get('blockname')
        urlfor = request.form.get('link')
        urlfor1 = request.form.get('name')
        block = bankuai(blockname=blockname, urlfor=urlfor, urlfor1=urlfor1)
        db.session.add(block)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/xueshu/<pid>')
@login_limit
def xueshu(pid):
    context = {
        'fatie': tiezi.query.filter(tiezi.blockid == '1').order_by(tiezi.zhutieTime.desc()).all()
    }
    tie=tiezi.query.filter(tiezi.blockid == '1').all()
    i=int(pid)
    zpid=int(len(tie)/5+1)
    zpids=[]
    while zpid!=0:
        zpids.append(zpid)
        zpid=zpid-1
    zpids = sorted(zpids)
    k=5*(i-1)
    j=5*i
    return render_template('xueshu.html', fatie=tie[k:j], zpids=zpids)

@app.route('/richang/')
@login_limit
def richang():
    context = {
        'fatie': tiezi.query.filter(tiezi.blockid == '2').order_by(tiezi.zhutieTime.desc()).all()
    }
    return render_template('richang.html', **context)

@app.route('/pl/<zhutie_id>/')
@login_limit
def pl(zhutie_id):
    blocks = bankuai.query.all()
    zhutie_model = tiezi.query.filter(tiezi.zhutieid == zhutie_id).first()
    usertel = session.get('usertel')
    userlimit = config.searchlimit(usertel)
    tzlimit = config.searchtzlimit(zhutie_id)
    blockid = config.tzidtoblock(zhutie_id)
    bkname = config.bkid2name(blockid)
    count = config.plcount(zhutie_id)
    users = User.query.filter(User.tel == usertel).first()
    uid = config.tzid2userid(zhutie_id)
    id = config.dhtoid(usertel)
    if userlimit >= tzlimit or uid == id:
        return render_template('pl.html', zhutie=zhutie_model, plcount=count, users=users, blocks=blocks)
    else:
        return render_template('LimitNone.html')

@app.route('/tieziup/<zhutieid>')
def tieziup(zhutieid):
    blocks = bankuai.query.all()
    config.tieziup(zhutieid)
    zhutie_model = tiezi.query.filter(tiezi.zhutieid == zhutieid).first()
    count = config.plcount(zhutieid)
    usertel = session.get('usertel')
    users = User.query.filter(User.tel == usertel).first()
    return redirect(url_for("pl", zhutie_id=zhutieid))

@app.route('/plup/<zt_id>/<pl_id>')
def plup(pl_id, zt_id):
    blocks = bankuai.query.all()
    config.plup(pl_id)
    zhutie_model = tiezi.query.filter(tiezi.zhutieid == zt_id).first()
    count = config.plcount(zt_id)
    usertel = session.get('usertel')
    users = User.query.filter(User.tel == usertel).first()
    return redirect(url_for("pl", zhutie_id=zt_id))


@app.route('/pldown/<zt_id>/<pl_id>')
def pldown(pl_id, zt_id):
    blocks = bankuai.query.all()
    config.pldown(pl_id)
    zhutie_model = tiezi.query.filter(tiezi.zhutieid == zt_id).first()
    count = config.plcount(zt_id)
    usertel = session.get('usertel')
    users = User.query.filter(User.tel == usertel).first()
    return redirect(url_for("pl", zhutie_id=zt_id))


@app.route('/search/', methods=['GET', 'POST'])
@login_limit
def search():
    blocks = bankuai.query.all()
    q = request.args.get('q')
    print(len(q))
    if len(q) != 0:
        tiezis = tiezi.query.filter(or_(tiezi.zhutietitle.contains(q), tiezi.zhutievalue.contains(q))).order_by(tiezi.zhutieTime.desc())
        return render_template('search.html', fatie=tiezis, blocks=blocks)
    else:
        return render_template('searchNone.html')

@app.route('/personal/<userid>')
def personal(userid):
    blocks = bankuai.query.all()
    usertel = session.get('usertel')
    id = config.dhtoid(usertel)
    user = User.query.filter(User.userid == userid).first()
    tiezis = tiezi.query.filter(tiezi.userid == userid).all()
    pl = pinglun.query.filter(pinglun.userid == userid).all()
    if userid == id:
        return render_template('personal.html', users=user, tiezis=tiezis, pls=pl, blocks=blocks)
    else:
        return render_template('tourist.html', users=user, tiezis=tiezis, pls=pl, blocks=blocks)

@app.route('/admin/', methods=['GET', 'POST'])
@login_limit
def admin():
    usertel = session.get('usertel')
    userlimit = config.searchlimit(usertel)
    if userlimit < 5:
        return render_template('LimitNone.html')
    blocks = bankuai.query.all()
    usertel = session.get('usertel')
    id = config.dhtoid(usertel)
    q1 = request.args.get('q1')
    if q1 == None:
        user = User.query.filter(User.tel == usertel).first()
        tiezis = tiezi.query.filter(tiezi.userid == id).all()
        pls = pinglun.query.filter(pinglun.userid == id).all()
        return render_template('admin.html', users=user, tiezis=tiezis, pls=pls, blocks=blocks)
    userss = User.query.filter(User.userid == q1).first()
    tieziss = tiezi.query.filter(tiezi.userid == q1).all()
    plss = pinglun.query.filter(pinglun.userid == q1).all()
    return render_template('admin.html', users=userss, tiezis=tieziss, pls=plss, blocks=blocks)

@app.route('/adminxiugai/<userid>', methods=['GET', 'POST'])
def adminxiugai(userid):
    blocks = bankuai.query.all()
    if request.method == 'GET':
        return render_template('adminxiugai.html', blocks=blocks)
    else:
        user = User.query.filter(User.userid == userid).first()
        limit = request.form.get('limit')
        pw = request.form.get('pw')
        name = request.form.get('username')
        if limit:
            user.userlimit = limit
        if pw:
            user.password = pw
        if name:
            user.username = name
        db.session.commit()
        user = User.query.filter(User.userid == userid).first()
        tiezis = tiezi.query.filter(tiezi.userid == userid).all()
        pls = pinglun.query.filter(pinglun.userid == userid).all()
        return redirect(url_for('admin', users=user, tiezis=tiezis, pls=pls, blocks=blocks))

@app.route('/delete/<tieziid>', methods=['GET', 'POST'])
def delete(tieziid):
    blockid = config.tzidtoblock(tieziid)
    tiezis = tiezi.query.filter(tiezi.zhutieid == tieziid).delete()
    db.session.commit()
    bkpl = config.bkplcount(blockid)
    bk1 = bankuai.query.filter(bankuai.blockid == blockid).first()
    bk1.plscount = bkpl
    db.session.add(bk1)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/deletepl/<plid>', methods=['GET', 'POST'])
def deletepl(plid):
    tieziid=config.plid2tzid(plid)
    blockid = config.tzidtoblock(tieziid)
    pl = pinglun.query.filter(pinglun.id == plid).delete()
    db.session.commit()
    bkpl = config.bkplcount(blockid)
    bk1 = bankuai.query.filter(bankuai.blockid == blockid).first()
    bk1.plscount = bkpl
    db.session.add(bk1)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/upload_file/', methods=['GET', 'POST'])
def upload_file():
    blocks = bankuai.query.all()
    usertel = session.get('usertel')
    id = config.dhtoid(usertel)
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, '%s.jpg'%(id)))
        user = User.query.filter(User.tel == usertel).first()
        user.touxiang = 1
        db.session.commit()
        return render_template('success.html', blocks=blocks)
    return render_template('upload_file.html', blocks=blocks)

@app.route('/xiugai/', methods=['GET', 'POST'])
def xiugai():
    blocks = bankuai.query.all()
    telephone = session.get('usertel')
    if request.method == 'GET':
        return render_template('xiugai.html', blocks=blocks)
    else:
        user = User.query.filter(User.tel == telephone).first()
        id = user.userid
        tiezis = tiezi.query.filter(tiezi.userid == id).first()
        pls = pinglun.query.filter(pinglun.userid == id).first()
        username = request.form.get('username')
        gender = request.form.get('gender')
        age = request.form.get('age')
        email = request.form.get('e-mail')
        if username:
            user.username = username
        if gender:
            user.gender = gender
        if age:
            user.age = age
        if email:
            user.email = email
        db.session.commit()
        user = User.query.filter(User.userid == id).first()
        tiezis = tiezi.query.filter(tiezi.userid == id).all()
        pls = pinglun.query.filter(pinglun.userid == id).all()
        return redirect(url_for('personal', userid=id))

@app.route('/addpl/', methods=['POST'])
def addpl():
    blocks = bankuai.query.all()
    content = request.form.get('pl-content')
    zhutie_id = request.form.get('zhutie_id')

    pls = pinglun(content=content)
    usertel = session.get("usertel")
    user = User.query.filter(User.tel == usertel).first()
    pls.author = user
    tiezis = tiezi.query.filter(tiezi.zhutieid == zhutie_id).first()
    pls.zhutie = tiezis
    db.session.add(pls)
    db.session.commit()
    blockid = config.tzidtoblock(zhutie_id)
    bkpl = config.bkplcount(blockid)
    bk1 = bankuai.query.filter(bankuai.blockid == blockid).first()
    bk1.plscount = bkpl
    db.session.add(bk1)
    db.session.commit()
    blocks1 = bankuai.query.all()
    return redirect(url_for('pl', zhutie_id=zhutie_id, blocks=blocks1))
@app.context_processor
def my_context_processor():

    '''userstel = session.get("usertel")
    if userstel:
        usern = config.sessionname(userstel)
        if usern:
            return {'username': usern}
    return {}'''
    usertel = session.get("usertel")
    if usertel:
        user = User.query.filter(User.tel == usertel).first()
        if user:
            return {'user': user}
    return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8090)
