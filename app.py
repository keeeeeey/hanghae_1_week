from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/write')
def home():
    return render_template('write.html')    

@app.route('/api/posting', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']   

    doc = {
        'user_id': id_receive,
        'user_pw': title_receive,
        'user_name': content_receive,
    }

    db.todolist.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '질문 등록 완료!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)