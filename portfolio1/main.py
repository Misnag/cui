from flask import render_template, request, url_for, render_template, redirect, jsonify, flash
from portfolio1 import app
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import ValidationError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

meal = {
    "0": ['日本料理','寿司','うどん','蕎麦','焼肉','しゃぶしゃぶ','海鮮','焼鳥','牛丼','定食'],
    "1": ['洋食','ハンバーガー','イタリア料理','カレー','フランス料理','カフェ','ステーキ','ピザ'],
    "2": ['中華料理','餃子','ラーメン','油そば','四川料理'],
    }
# すべてのvalueを対象にした新しいkeyを作成
meal["100"] = [value for values in meal.values() for value in values]

# DB機能
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

db_uri = 'sqlite:///login.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class User(db.Model, UserMixin):
    __tableaccountid__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    accountid = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    formatted_address = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    formatted_address = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class LoginForm(FlaskForm):
    accountid = StringField('ID')
    password = StringField('パスワード')
    submit = SubmitField('ログイン')
    
class SignupForm(FlaskForm):
    accountid = StringField('ID')
    password = StringField('パスワード')
    submit = SubmitField('アカウント登録')
  
class LikeForm(FlaskForm):
    name = HiddenField()
    formatted_address = HiddenField()
    favorite = SubmitField('♡ お気に入り', id='favorite')

class ReviewForm(FlaskForm):
    name = HiddenField()
    formatted_address = HiddenField()
    rating = HiddenField()
    comment = StringField('コメント')
    submit = SubmitField('レビューを保存')

def validate_id(self, accountid):
    if User.query.filter_by(accountid=accountid.data).one_or_none():
        raise ValidationError('このIDは使用できません')
  
@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None' or user_id is None:
        redirect('/login')
    else:
        return User.query.get(int(user_id))


# トップページを表示
@app.route('/')
def index():
    return render_template('portfolio1/index.html', meal=meal)

# indexから条件取得し、結果表示画面に渡す
@app.route('/result', methods=['POST'])
def result():
    data = request.form
    selected_meal = data['selected-data']
    address = request.form['address']
    form1 = LikeForm()
    form2 = ReviewForm()
    return render_template('portfolio1/result.html', selected_meal=selected_meal, address=address, form1=form1, form2=form2)

# アカウント作成機能
@app.route('/account')
@login_required
def account():
    likes = Like.query.filter_by(user_id=current_user.id).all()
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    form2 = ReviewForm()
    return render_template('portfolio1/account.html', accountid=current_user.accountid, likes=likes, reviews=reviews, form2=form2)


@app.route('/signup', methods=['GET','POST'])
def signup():
    signup = SignupForm()
    if signup.validate_on_submit():
        newuser = User(accountid=signup.accountid.data, password=signup.password.data)
        db.session.add(newuser)
        db.session.commit()
        return redirect('/login')
    return render_template('portfolio1/signup.html', signup=signup)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(accountid=form.accountid.data, password=form.password.data).one_or_none():
            user = User.query.filter_by(accountid=form.accountid.data).one_or_none()
            login_user(user)
            return redirect('/account')
        else:
            return 'ログインに失敗しました'
    return render_template('portfolio1/login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template('portfolio1/logout.html')

# お気に入り機能
@app.route('/like', methods=['POST'])
def like():
    form = LikeForm()
    if form.validate_on_submit():
        like = Like(
            user_id=current_user.id,
            name=form.name.data,
            formatted_address=form.formatted_address.data,
        )
        db.session.add(like)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'errors': form.errors})

# 削除機能
@app.route('/like/<int:like_id>/delete', methods=['POST'])
@login_required
def delete_like(like_id):
    like = Like.query.get_or_404(like_id)
    db.session.delete(like)
    db.session.commit()
    flash('Your like has been deleted.', 'success')
    return redirect(url_for('account'))

# レビュー機能
@app.route('/review', methods=['POST'])
def review():
    form2 = ReviewForm()
    if form2.validate_on_submit():
        review.rating = int(form2.rating.data)
        review.comment = form2.comment.data
        db.session.commit()
        return redirect(url_for('detail', name=review.name, formatted_address=review.formatted_address))

    form2.name.data = review.name
    form2.formatted_address.data = review.formatted_address
    form2.rating.data = str(review.rating) if review.rating else ''
    form2.comment.data = review.comment

    return render_template('portfolio1/account.html', form2=form2)

# dbのレビュー内容を変更
@app.route('/review/edit/<int:review_id>', methods=['GET','POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    form2 = ReviewForm(obj=review)

    if form2.validate_on_submit():
        review.rating = form2.rating.data
        review.comment = form2.comment.data
        db.session.commit()
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form2.rating.data = review.rating
        form2.comment.data = review.comment
        form2.date_posted.data = review.date_posted 
    
    return render_template('portfolio1/account.html', form2=form2, review=review, review_id=review_id)

# 削除機能
@app.route('/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted.', 'success')
    return redirect(url_for('account'))

# レビュー、お気に入り一覧にある店の名前をクリックすると、結果表示ページに飛ぶ
@app.route('/detail', methods=['POST'])
def detail():
    selected_meal = request.form.get('name')
    address = request.form.get('formatted_address')
    form1 = LikeForm()
    form2 = ReviewForm()
    return render_template('portfolio1/result.html', selected_meal=selected_meal, address=address, form1=form1, form2=form2)


# 既に存在するレビュー、お気に入りのデータがdbにあるかAjax,JSONで確認
@app.route('/check_like', methods=['POST'])
def check_like():
    name = request.form.get('name')
    formatted_address = request.form.get('formatted_address')
    like_exists = False
    record = Like.query.filter_by(user_id=current_user.id, name=name, formatted_address=formatted_address).first()

    if record:
        like_exists = True
    return jsonify({'exists': str(like_exists)})

@app.route('/check_review', methods=['POST'])
def check_review():
    name = request.form.get('name')
    formatted_address = request.form.get('formatted_address')
    review_exists = False
    record = Review.query.filter_by(user_id=current_user.id, name=name, formatted_address=formatted_address).first()

    if record:
        review_exists = True
        rating = record.rating
        comment = record.comment
        return jsonify({'exists': str(review_exists), 'rating': rating, 'comment': comment})
    else:
        return jsonify({'exists': str(review_exists)})
