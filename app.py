from bson import ObjectId
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib

# client = MongoClient('mongodb://test:test@localhost', 27017)

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbhanghae

SECRET_KEY = 'SPARTA'


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

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        print("비로그인 to index")
        return render_template('index.html', list=question_list)
    else:
        print("로그인 to index")
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.users.find_one({"id": payload['id']})['id']

            return render_template('index.html', list=question_list, userId=user_id)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))


## 글쓰기화면 보여주기
@app.route('/write')
def write():
    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')
    user_id = request.args.get('user_id')
    # if token_receive is None:
    #     print("비로그인 to index")
    #     return render_template('login.html')
    # else:
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_id = db.users.find_one({"id": payload['id']})['id']
    #
    #     return render_template('write.html', userId=user_id)
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login"))

    return render_template('write.html', userId=user_id)


## 글쓰기화면 보여주기
@app.route('/login')
def login():
    return render_template('login.html')


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

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')
    print('article_id : ' + article_id)
    target_article = db.article.find_one({'_id': ObjectId(article_id)})
    # print('target_article : ' + str(target_article))
    # reply_on_article = list(db.reply.find({'article_id', article_id}, {'_id':False}))
    # print('reply on article : ' + str(reply_on_article))
    user_checker = True
    return render_template('read.html', target_article=target_article, user_checker=user_checker)
    # if token_receive is None:
    #     print("비로그인 to index")
    #     return render_template('login.html')
    # else:
    #     print("로그인 to index")
    #     try:
    #         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #         user_id = db.users.find_one({"id": payload['id']})['id']
    #
    #         target_article = db.article.find_one({'_id': ObjectId(article_id)})
    #         reply_on_article = list(db.reply.find({'article_id', article_id}))
    #
    #         user_checker = False
    #
    #         if target_article[user_id] == user_id:
    #             user_checker = True
    #         print('render_template : to read.html')
    #         return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article,
    #                                user_checker=user_checker)
    #     except jwt.ExpiredSignatureError:
    #         return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    #     except jwt.exceptions.DecodeError:
    #         return redirect(url_for("login"))

## 글쓰기화면 보여주기
@app.route('/write')
def move_write():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #지정된 token id filed
    user_info = db.article.find_one({"user_id": payload['id']})
    return render_template('write.html', user_id = user_info["user_id"])

@app.route('/api/posting', methods=['POST'])
def write_post():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {
        'user_id': id_receive,
        'title': title_receive,
        'content': content_receive,
    }

    db.article.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '질문 등록 완료!!'})


## 글쓰기화면 보여주기
@app.route('/readPage')
def readPage():
    # article = list(db.article.find({}, {'_id': False}))
    return render_template('read.html')

## register 화면 보여주기
@app.route('/registerPage')
def registerPage():
    return render_template('register.html')

## 로그인 API
@app.route('/api/login', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    print(username_receive)
    print(password_receive)

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})
    print('check login result : ' + result)
    if result is not None:
        payload = {
        'id': username_receive,
        'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'mytoken': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

## id 중복검사
@app.route('/api/idCheck', methods=['POST'])
def idCheck():
    id_receive = request.form['id_give']
    exists = bool(db.user.find_one({"id": id_receive}))
    return jsonify({'result': 'success', 'exists': exists})

## nickname 중복검사
@app.route('/api/nicknameCheck', methods=['POST'])
def nicknameCheck():
    nickname_receive = request.form['nickname_give']
    exists = bool(db.user.find_one({"nickname": nickname_receive}))
    return jsonify({'result': 'success', 'exists': exists})

## 회원가입
@app.route('/api/register', methods=['POST'])
def register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']
    email_receive = request.form['email_give']
    zipcode_receive = request.form['zipcode_give']
    address_receive = request.form['address_give']
    detail_receive = request.form['detail_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,
        "password": pw_hash,
        "nickname": nickname_receive,
        "email": email_receive,
        "zipcode": zipcode_receive,
        "address": address_receive,
        "detail": detail_receive,
    }
    db.user.insert_one(doc)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)