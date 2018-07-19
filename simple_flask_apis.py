from flask import Flask
from flask import render_template
import json
from flask import abort
from flask import jsonify
from flask import make_response
from flask import request

'''
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
'''

app=Flask(__name__)

tasks = [
    {
        "id":1,
        "title":"task_1",
        "description":"task 1"
    },
    {
        "id":2,
        "title":"API 2",
        "description":"flask api 2"
    }
]

emotions = [
    {
        "id":1,
        "type":'daxiao',
        "img_url":'daxiao_url',
        "animation_url":'daxiao_a__url'
    },
    {
        "id":2,
        "type":'yinxian',
        "img_url":'yinxian_url',
        "animation_url":'yinxian_a_url',
    },
    {
        "id":3,
        "type": 'kuqi',
        "img_url": 'kuqi_url',
        "animation_url": 'kuqi_a_url',
    }
]

@app.route('/hello')
def get_default():
    return "hello world"

@app.route('/tasks/<int:task_id>', methods=['GET'])
def task_1(task_id):
    # filter接收一个函数f和一个list，通过函数f对list中每个元素判断，返回true或false，过滤掉不需要的元素
    task = list(filter(lambda t:t['id'] == task_id, tasks))
    if len(task)==0:
        abort(404)
    return jsonify({'tasks':task[0]})

@app.route('/emotion/<emotion>',methods=['GET'])
def emotion_s(emotion):
    emo = list(filter(lambda em:em['type']==emotion,emotions))
    if len(emo)==0:
        abort(404)
    return jsonify({'emotion': emo[0]})  # 构造字典

@app.route('/emotion', methods=['GET'])
def emo():
    return jsonify({'emotions': emotions})

@app.route("/emotion", methods=['POST'])
def emo_post():
    # print(request.form["emotion"])
    # 判断是否有json数据post
    if not request.json:
        abort(400)
    # post过来的json数据是bytes类型，先解码为json字符串，再将字符串转换为字典
    req_d=json.loads(request.get_data().decode())
    # print(req_d)

    if not req_d or not "emotion" in req_d:
        abort(400)
    re_j_emo=req_d["emotion"]
    emo = list(filter(lambda emo:emo['type']==re_j_emo, emotions))
    if not len(emo):
        emo_new={
           "id":emotions[-1]['id']+1,
            "type":re_j_emo,
            "img_url":"/emotion/"+re_j_emo,
            "animation_url":"animation_a_url"
        }
        emotions.append(emo_new)
        return jsonify({"emotion new":emo_new})
    else:
        return jsonify({"emotion":emo[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

if __name__=="__main__":
    host = '192.168.31.128'
    port = '5000'
    app.run(host='0.0.0.0', port=port, debug=False)
