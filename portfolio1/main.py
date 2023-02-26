from portfolio1 import app
from flask import render_template, request

meal = {
    "0": ['日本料理','寿司','うどん','蕎麦','焼肉','しゃぶしゃぶ','海鮮','焼鳥','丼'],
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
@app.route('/stop', methods=['POST'])
def stop():
    data = request.json
    selectedData = data.get('selectedData')
    address = request.form['address']
    result = {
        'selected_meal': selectedData,
        'address': address,
    }
    return render_template('portfolio1/result.html', result = result)

# マイページ(まだ)
@app.route('/memberpage')
def memberpage():
    return render_template('memberpage.html')
