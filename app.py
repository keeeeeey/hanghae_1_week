from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import jwt
import datetime
import hashlib

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.dbhanghae

SECRET_KEY = 'SPARTA'

## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
    result = db.user.find_one({'username': username_receive, 'password': pw_hash})

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