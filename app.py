from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    print("home start")

    question_list = list(db.article.find({}, {'_id': False}))

    return render_template('index.html', list=question_list)


## 글쓰기화면 보여주기
@app.route('/write')
def write():
    return render_template('write.html')


## 글쓰기화면 보여주기
@app.route('/login')
def login():
    return render_template('login.html')


## 글쓰기화면 보여주기
@app.route('/api/search', methods=['POST'])
def search():
    words_receive = request.form['words_give']

    find_list = list(db.article.find({'title':{'$regex':words_receive, '$options' : 'i'}},{'_id': False}))

    for i in range(len(find_list)):
        print("find : " + str(find_list[i]))

    return jsonify({'searched_list': find_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)