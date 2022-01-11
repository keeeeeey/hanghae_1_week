import math

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

    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 10

    list_all = list(db.article.find({}))

    # 게시물의 총 개수 세기
    tot_count = len(list_all)
    print(tot_count)
    # 마지막 페이지의 수 구하기
    last_page_num = math.ceil(tot_count / limit)  # 반드시 올림을 해줘야함

    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    question_list = list(db.article.find({}).skip((page - 1) * limit).limit(limit))
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
        return render_template('index.html', list=question_list, limit=limit, page=page, block_start=block_start, block_end=block_end, last_page_num=last_page_num)
    else:
        print("로그인 to index" + token_receive)
        try:
            print('try: ')
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']

            print('list : ' + str(question_list) + ' user_id : ' + user_id)

            return render_template('index.html', list=question_list, userId=user_id, limit=limit, page=page, block_start=block_start, block_end=block_end, last_page_num=last_page_num)
        except jwt.ExpiredSignatureError:
            print('case1')
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            print('case2')
            return redirect(url_for("login"))


## 글쓰기화면 보여주기
@app.route('/write')
def write():
    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')
    # user_id = request.args.get('user_id')
    if token_receive is None:
        print("비로그인 to index")
        return render_template('login.html')
    else:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']
            print('user_id : ' + user_id)
            return render_template('write.html', user_id=user_id)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))

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

    # user_checker = True
    # return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article, user_checker=user_checker)
    if token_receive is None:
        print("비로그인 to read")
        return render_template('login.html')
    else:
        print("로그인 to read")
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']

            target_article = db.article.find_one({'_id': ObjectId(article_id)})
            reply_on_article = list(db.reply.find({'article_id':{'$regex':article_id}}))
            print('target article : ' + str(target_article))
            user_checker = False

            if target_article['user_id'] == user_id:
                user_checker = True
            print('render_template : to read.html')
            return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article,
                                   user_checker=user_checker)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))



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

## 글 삭제하기
@app.route('/api/delete', methods=['POST'])
def delete_article():
    articleID_receive = request.form['articleID_give']
    db.article.delete_one({'_id': ObjectId(articleID_receive)})
    return jsonify({'result': 'success', 'msg': '삭제되었습니다'})

## 로그인 API
@app.route('/api/login', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
        'id': username_receive,
        'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
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