from flask import render_template, request
from portfolio1 import app
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy


meal = {
    "0": ['日本料理','寿司','うどん','蕎麦','焼肉','しゃぶしゃぶ','海鮮','焼鳥','牛丼','定食'],
    "1": ['洋食','ハンバーガー','イタリア料理','カレー','フランス料理','カフェ','ステーキ','ピザ'],
    "2": ['中華料理','餃子','ラーメン','油そば','四川料理'],
    }
# すべてのvalueを対象にした新しいkeyを作成
meal["100"] = [value for values in meal.values() for value in values]


# ログイン機能
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

db_uri = 'sqlite:///login.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    mail = db.Column(db.Text())
    def __init__(self, name, mail):
      self.name = name
      self.mail = mail

db.create_all()

class LoginForm(FlaskForm):
    name = StringField('名前')
    mail = StringField('メールアドレス')
    submit = SubmitField('ログイン')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# トップページを表示
@app.route('/')
def index():
    return render_template('portfolio1/index.html', meal=meal)

# indexから条件取得
@app.route('/result', methods=['POST'])
def result():
    data = request.form
    selected_meal = data['selected-data']
    address = request.form['address']
    return render_template('portfolio1/result.html', selected_meal=selected_meal, address=address)


@app.route('/member')
@login_required
def member():
    return render_template('portfolio1/member.html')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.name.data == 'cui' and form.mail.data == 'cui':
            user = User(form.name.data)
            login_user(user)
            return redirect('/member')
        else:
            return 'ログインに失敗しました'
    return render_template('portfolio1/login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('portfolio1/logout.html')
