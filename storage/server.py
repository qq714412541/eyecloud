# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import time
import json

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello 尼古拉斯赵四'


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':


        data = request.form.to_dict()
        taskid = data['taskid']
        reportid = data['reportid']
        name = data['name']
        doc = open('test.txt', 'w')

        print(str(taskid), file=doc)
        print(str(reportid), file=doc)
        print(str(name), file=doc)


        status = 200

        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('localtime=' + localtime)
        # 系统当前时间年份
        year = time.strftime('%Y', time.localtime(time.time()))
        # 月份
        month = time.strftime('%m', time.localtime(time.time()))
        # 日期
        day = time.strftime('%d', time.localtime(time.time()))
        # 具体时间 小时分钟毫秒
        hms = time.strftime('%H%M%S', time.localtime(time.time()))
        fileYear = os.getcwd() + '/' + year
        fileMonth = fileYear + '/' + month
        fileDay = fileMonth + '/' + day
        fileSecond = fileDay + '/' + hms
        if not os.path.exists(fileYear):
            os.mkdir(fileYear)
            os.mkdir(fileMonth)
            os.mkdir(fileDay)
            os.mkdir(fileSecond)
        else:
            if not os.path.exists(fileMonth):
                os.mkdir(fileMonth)
                os.mkdir(fileDay)
                os.mkdir(fileSecond)
            else:
                if not os.path.exists(fileDay):
                    os.mkdir(fileDay)
                    os.mkdir(fileSecond)
                else:
                    if not os.path.exists((fileSecond)):
                        os.mkdir(fileSecond)
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, fileSecond,
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        response = {
            'code': 400
        }

        return jsonify(response), status









if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
