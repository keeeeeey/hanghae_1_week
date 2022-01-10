from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    print("home start")

    question_list = list(db.article.find({}))
    id_list = []

    #id값을 가져올 수 있도록 articles의 ObjectId로 되어있는 _id를 str형식으로 변경한다.
    for item in question_list:
        id_list.append(str(item['_id']))

    for i in range(len(question_list)):
        del question_list[i]['_id']
        question_list[i]['_id'] = id_list[i]

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


## 글쓰기화면 보여주기
@app.route('/api/search', methods=['POST'])
def search():
    words_receive = request.form['words_give']

    find_list = list(db.article.find({'title':{'$regex':words_receive, '$options' : 'i'}}))

    id_list = []

    # id값을 가져올 수 있도록 articles의 ObjectId로 되어있는 _id를 str형식으로 변경한다.
    for item in find_list:
        id_list.append(str(item['_id']))

    for i in range(len(find_list)):
        del find_list[i]['_id']
        find_list[i]['_id'] = id_list[i]

    return jsonify({'searched_list': find_list})


## 글쓰기화면 보여주기
@app.route('/api/read')
def read():

    article_id = request.args.get('article_id')
    user_id = request.args.get('user_id')

    target_article = db.article.find_one({'_id': article_id})
    reply_on_article = list(db.reply.find({'article_id', article_id}))

    return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)