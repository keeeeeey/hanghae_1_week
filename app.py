import math
from bson import ObjectId, objectid
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib

client = MongoClient('mongodb://test:test@localhost', 27017)

app = Flask(__name__)
#client = MongoClient('localhost', 27017)
db = client.dbhanghae

SECRET_KEY = 'SPARTA'

## HTML 화면 보여주기
@app.route('/')
def homework():
    print("home start")

    sortingType = request.args.get("sortingType")
    print(sortingType)

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

    question_list = list(db.article.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit))
    if sortingType == "hits":
        question_list = list(db.article.find({}).sort("count",-1).skip((page - 1) * limit).limit(limit))
    else:
        question_list = list(db.article.find({}).sort("_id", -1).skip((page - 1) * limit).limit(limit))
    print('question list : ' + str(question_list))
    id_list = []

    # id값을 가져올 수 있도록 articles의 ObjectId로 되어있는 _id를 str형식으로 변경한다.
    for item in question_list:
        id_list.append(str(item['_id']))

    for i in range(len(question_list)):
        del question_list[i]['_id']
        question_list[i]['_id'] = id_list[i]

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        print("비로그인 to index")

        return render_template('index.html', list=question_list, limit=limit, page=page, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num)

    else:
        print("로그인 to index" + token_receive)
        try:
            print('try: ')
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})['id']
            user_nickname = db.user.find_one({"id": payload['id']})['nickname']

            print('list : ' + str(question_list) + ' user_id : ' + user_id)

            return render_template('index.html', list=question_list, userId=user_id, userNickname=user_nickname,
                                   limit=limit, page=page, block_start=block_start, block_end=block_end,
                                   last_page_num=last_page_num)

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

## 로그인 화면 보여주기
@app.route('/login')
def login():
    return render_template('login.html')


## 글쓰기화면 보여주기
@app.route('/api/search', methods=['POST'])
def search():
    words_receive = request.form['words_give']

    find_list = list(db.article.find({'title':{'$regex':words_receive, '$options' : 'i'}}))
    #'$option' : 'i' =>  대소문자를 구분하지 않는 정규식 일치 수행

    id_list = []

    # id값을 가져올 수 있도록 articles의 ObjectId로 되어있는 _id를 str형식으로 변경한다.
    for item in find_list:
        id_list.append(str(item['_id']))

    #find_list의 '_id' 값을 string으로 conver 후 id_list에 append
    for i in range(len(find_list)):
        del find_list[i]['_id']
        find_list[i]['_id'] = id_list[i]
    #정규식에 일치하는 값들만 빼옴

    return jsonify({'searched_list': find_list})

## mypage 화면
@app.route('/api/mypage')
def toMypage():
    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        print("비로그인 to read")
        return render_template('login.html')
    else:
        print("로그인 to read")
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_id = db.user.find_one({"id": payload['id']})

            return render_template('mypage.html', userId=user_id)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))


## 회원정보 수정
@app.route('/api/updateMember', methods=['POST'])
def updateMember():
    user_pw = request.form['pw_give']
    user_zipcode = request.form['zipcode_give']
    user_address = request.form['address_give']
    user_detail = request.form['detail_give']

    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    if token_receive is None:
        print("비로그인 to read")
        return render_template('login.html')
    else:
        print("로그인 to read")
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            db.user.update_many({'id': payload['id']}, {
                '$set': {'password': pw_hash, 'zipcode': user_zipcode, 'address': user_address, 'detail': user_detail}})
            return jsonify({'result': 'success'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))

## 글쓰기화면 보여주기
@app.route('/api/read')
def read():
    article_id = request.args.get('article_id')
    # jwt token 받아오기
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = db.user.find_one({"id": payload['id']})['id']
        # 글 제목, 내용 불러오기
        target_article = db.article.find_one({'_id': ObjectId(article_id)})
        # 해당 글의 댓글 불러오기
        reply_on_article = list(db.reply.find({'article_id': {'$regex': article_id}}))

        ##조회수 추가 함수
        count = target_article['count'] + 1
        db.article.update_one({'_id': ObjectId(article_id)}, {'$set': {'count': count}})

        # 페이지 값 (디폴트값 = 1)
        page = request.args.get("page", 1, type=int)
        # 한 페이지 당 몇 개의 게시물을 출력할 것인가
        limit = 10

        target_article = db.article.find_one({'_id': ObjectId(article_id)})
        all_reply = list(db.reply.find({'article_id': {'$regex': article_id}}))

        reply_on_article = list(
            db.reply.find({'article_id': {'$regex': article_id}}).sort('good', 1).skip((page - 1) * limit).limit(limit))

        # 게시물의 총 개수 세기
        tot_count = len(all_reply)

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

        user_checker = False
        reply_like_list = []

        # 댓글들의 좋아요 명단 가져오기
        if reply_on_article != '':
            for item in reply_on_article:
                like_list = item['good_bad']
                print("list : " + str(like_list))
                if user_id in like_list:
                    user_checker = True
                else:
                    user_checker = False
                reply_like_list.append(user_checker)

        for i in range(len(reply_on_article)):
            reply_on_article[i]['like_checker'] = reply_like_list[i]

        print('reply_like_list : ' + str(reply_like_list))
        print('reply_on_article : ' + str(reply_on_article))

        user_checker = False
        if target_article['user_id'] == user_id:
            user_checker = True
        print('render_template : to read.html')

        # 정렬
        reply_on_article = sorted(reply_on_article, key=lambda item: (-int(item['good'])))
        print('target article : ' + str(target_article['user_id']) + ', user_id : ' + user_id)
        print('go return to read : ' + str(reply_on_article))
        print('user_checker : ' + str(user_checker))
        return render_template('read.html', target_article=target_article, reply_on_article=reply_on_article,
                               user_checker=user_checker, limit=limit, page=page, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num, user_id=user_id)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))

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
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

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
    print('write_post start')
    id_receive = request.form['id_give']
    print('id : ' + id_receive)
    title_receive = request.form['title_give']
    print('title : ' + title_receive)
    content_receive = request.form['content_give']
    print('receive data : ' + content_receive)
    image_checker = request.form['image_checker']
    print('image_checker=' + image_checker)

    if image_checker == 'true':
        image = request.files['image']
        extension = image.filename.split('.')
        print('extension : ' + str(extension))
        today = datetime.now()
        mytime = today.strftime('%Yy%mm%dd%H:%M:%S')
        filename = f'{mytime}-{extension[0]}'
        filename = "".join(i for i in filename if i not in "\/:*?<>|")
        filename = filename.strip()
        print('filename : ' + filename)
        save_to = f'static/images/{filename}.{extension[1]}.jpg'
        image.save(save_to)
        print('which one')
        doc = {
            'user_id': id_receive,
            'title': title_receive,
            'contents': content_receive,
            'imageUrl': f'{filename}.{extension[1]}.jpg',
            'count': 0
        }
    else:
        doc = {
            'user_id': id_receive,
            'title': title_receive,
            'contents': content_receive,
            'count': 0
        }

    db.article.insert_one(doc)
    print('done, anyway')
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
    print('like check-1')
    id_receive = request.form['id_give']
    checker = request.form['checker']
    target_reply = db.reply.find_one({'_id': ObjectId(id_receive)})
    good = target_reply['good']
    good = int(good)
    print('like check0')
    # 좋아요한 명단 불러오기
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_id = db.user.find_one({"id": payload['id']})['id']
    like_list = target_reply['good_bad']
    print('like check1' + checker)
    # 좋아요를 누른 경우
    if checker == 'true':
        if user_id in like_list:
            print('like but err')
            return jsonify({'result': 'success', 'msg': '잠시 후 다시 시도해주세요.'})
        else:
            print('like good')
            good += 1
            like_list.append(user_id)

    # 좋아요 취소를 누른 경우
    else:
        for i in range(len(like_list)):
            if like_list[i] == user_id:
                del like_list[i]
                good -= 1
                print('like bad')
                break

    print('like : ' + str(like_list))
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
                'user_id': user_id,
                'reply_data': reply_receive,
                'good': '0',
                'good_bad': []
            }

            db.reply.insert_one(doc)

            print('user_id : ' + user_id)
            return jsonify({'result': 'success', 'msg': '답변 작성이 완료되었습니다!'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))


@app.route('/api/deleteReply', methods=['POST'])
def del_reply():
    reply_id_receive = request.form['reply_id_give']

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

            target = db.reply.find_one({'_id': ObjectId(reply_id_receive)})

            if target['user_id'] == user_id:
                db.reply.delete_one({'_id': ObjectId(reply_id_receive)})

            print('user_id : ' + user_id)
            return jsonify({'result': 'success', 'msg': '삭제가 완료되었습니다!'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))


@app.route('/api/modifyReply', methods=['POST'])
def modify_reply():
    reply_id_receive = request.form['reply_id_give']
    modify_value = request.form['modify_value']

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

            target = db.reply.find_one({'_id': ObjectId(reply_id_receive)})

            if target['user_id'] == user_id:
                db.reply.update_one({'_id': ObjectId(reply_id_receive)}, {'$set': {'reply_data': modify_value}})

            print('user_id : ' + user_id)
            return jsonify({'result': 'success', 'msg': '수정이 완료되었습니다!'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login"))


## 수정
@app.route('/api/update', methods=['POST'])
def update_posting():
    
    id_receive = str(request.form['id_give']) 
    print('id_receive : ' + id_receive)
    id_convert = ObjectId(id_receive);    
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    db.article.update_one({'_id':id_convert},{'$set':{'title': title_receive,'contents': content_receive}})

    return jsonify({'result': 'success'})      

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)