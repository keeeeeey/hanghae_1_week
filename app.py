from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.dbhomework

SECRET_KEY = 'SPARTA'

import jwt

## main page url
@app.route('/')
def home():
    return render_template('index.html')

## write page url   
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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)