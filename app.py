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
        print("로그인 to index" + token_receive)
        try:
            print('try: ')
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']
            print('list : ' + str(question_list) + ' user_id : ' + user_id)
            return render_template('index.html', list=question_list, userId=user_id)
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
        print("비로그인 to write")
        return render_template('login.html')
    else:
        try:
            print("로그인 to write")
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
            #글 제목, 내용 불러오기
            target_article = db.article.find_one({'_id': ObjectId(article_id)})
            #해당 글의 댓글 불러오기
            reply_on_article = list(db.reply.find({'article_id':{'$regex':article_id}}))
            print('target article : ' + str(target_article))
            user_checker = False
            print('reply_on_article : ' + str(reply_on_article))
            reply_like_list = []

            #댓글들의 좋아요 명단 가져오기
            for item in reply_on_article:
                like_list = item['good_bad']

                if user_id in like_list:
                    print('get in for : ')
                    user_checker = True
                    print('user_id : ' + user_id)
                    print('user_checker : ' + str(user_checker))
                else:
                    user_checker=False
                reply_like_list.append(user_checker)
                user_checker=False

            for i in range(len(reply_on_article)):
                reply_on_article[i]['like_checker'] = reply_like_list[i]
            print('reply_like_list : ' + str(reply_like_list))
            print('reply_on_article : ' + str(reply_on_article))
            if target_article['user_id'] == user_id:
                user_checker = True
            print('render_template : to read.html')
            return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article,
                                   user_checker=user_checker)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))

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


@app.route('/api/posting', methods=['POST'])
def write_post():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']   

    doc = {
        'user_id': id_receive,
        'title': title_receive,
        'contents': content_receive,
    }

    db.article.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '질문 등록 완료!!'})


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


@app.route('/api/like', methods=['POST'])
def like():
    id_receive = request.form['id_give']
    checker = request.form['checker']
    target_reply = db.reply.find_one({'_id': ObjectId(id_receive)})
    good = target_reply['good']
    good = int(good)

    # 좋아요한 명단 불러오기
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_id = db.user.find_one({"id": payload['id']})['id']
    like_list = target_reply['good_bad']

    #좋아요를 누른 경우
    if checker=='true':

        if user_id in like_list:
            return jsonify({'result': 'success', 'msg': '잠시 후 다시 시도해주세요.'})
        else:
            good += 1
            like_list.append(user_id)

    #좋아요 취소를 누른 경우
    else:
        for i in range(len(like_list)):
            if like_list[i] == user_id:
                del like_list[i]
                good -= 1
                break

    db.reply.update_one({'_id': ObjectId(id_receive)}, {'$set': {'good_bad': like_list}})
    db.reply.update_one({'_id': ObjectId(id_receive)}, {'$set': {'good': str(good)}})

    return jsonify({'result': 'success', 'msg': '!'})


@app.route('/api/setReply', methods=['POST'])
def add_reply():

    articleID_receive = request.form['articleID_give']
    reply_receive = request.form['reply_give']

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')
    # user_id = request.args.get('user_id')
    if token_receive is None:
        print("비로그인 to write")
        return render_template('login.html')
    else:
        try:
            print("로그인 to write")
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']

            doc = {
                'article_id': articleID_receive,
                'user_id' : user_id,
                'reply_data': reply_receive,
                'good' : '0'
            }

            db.reply.insert_one(doc)

            print('user_id : ' + user_id)
            return jsonify({'result': 'success', 'msg': '답변 작성이 완료되었습니다!'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))

    return jsonify({'result': 'success', 'msg': '질문 등록 완료!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)