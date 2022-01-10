from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework

## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)