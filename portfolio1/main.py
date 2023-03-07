from flask import render_template, request, redirect, url_for
from portfolio1 import app
from portfolio1 import db
from portfolio1.models.account import Account

meal = {
    "0": ['日本料理','寿司','うどん','蕎麦','焼肉','しゃぶしゃぶ','海鮮','焼鳥','牛丼','定食'],
    "1": ['洋食','ハンバーガー','イタリア料理','カレー','フランス料理','カフェ','ステーキ','ピザ'],
    "2": ['中華料理','餃子','ラーメン','油そば','四川料理'],
    }
# すべてのvalueを対象にした新しいkeyを作成
meal["100"] = [value for values in meal.values() for value in values]

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


# ログイン機能
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('portfolio1/signup.html')
    if request.method == 'POST':
        form_name = request.form.get('name')
        form_id = request.form.get('id')
        form_password = request.form.get('password')

        account = Account(
            name=form_name,
            id=form_id,
            password=form_password,
        )
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/accounts')
def account_list():
    accounts = Account.query.all()
    return render_template('portfolio1/account_list.html', accounts=accounts)


@app.route('/accounts/<int:id>')
def account_detail(id):
    account = Account.query.get(id)
    return render_template('portfolio1/account_detail.html', account=account)

# 編集ページ表示用
@app.route('/accounts/<int:id>/edit', methods=['GET'])
def account_edit(id):
    account = Account.query.get(id)
    return render_template('portfolio1/account_edit.html', account=account)


@app.route('/accounts/<int:id>/update', methods=['POST'])
def account_update(id):
    account = Account.query.get(id)
    account.name = request.form.get('name')
    account.id = request.form.get('id')
    account.password = request.form.get('password')

    db.session.merge(account)
    db.session.commit()
    return redirect(url_for('account_list'))


@app.route('/accounts/<int:id>/delete', methods=['POST'])  
def account_delete(id):  
    account = Account.query.get(id)   
    db.session.delete(account)  
    db.session.commit()  
    return redirect(url_for('account_list'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('portfolio1/login.html')
    if request.method == 'POST':
        form_name = request.form.get('name')
        form_id = request.form.get('id')
        form_password = request.form.get('password')

        account = Account(
            name=form_name,
            id=form_id,
            password=form_password,
        )
        db.session.add(account)
        db.session.commit()
        return redirect(url_for('index'))