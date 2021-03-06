# -*- coding:utf-8 -*
import logging
import hashlib
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, Response
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from myWerobot import myrobot
from werobot.contrib.flask import make_view
logging.basicConfig(filename="./flask.log")
# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__,static_folder="/root/edu")
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        project = request.form.get("project","")
        img_type = request.form.get("type","")
        tag = request.form.get("tag","")


        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        img_src = os.path.join(basepath,"static/images",project,img_type,tag)
        os.makedirs(img_src)

        upload_path = os.path.join(img_src, secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        image_data = open(upload_path, "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response

    return render_template('upload.html')

@app.route('/down/<path:img_url>', methods=['POST', 'GET'])  # 添加路由
def down_img (img_url):
    basepath = os.path.dirname(__file__)  # 当前文件所在路径

    upload_path = os.path.join(basepath, 'static/images', img_url)
    image_data = open(upload_path, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/image/<imageid>")
def index(imageid):
    image = open("丽江/{}.jpg".format(imageid))
    resp = Response(image, mimetype="image/jpeg")
    return resp


@app.route('/wx_pub',methods=['GET','POST'])
def wx():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    token = "xiaofeishu"
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    sha1.update(list[0].encode('utf-8'))
    sha1.update(list[1].encode('utf-8'))
    sha1.update(list[2].encode('utf-8'))
    hashcode = sha1.hexdigest()
    logging.info("handle/GET func: hashcode, signature, timestamp, nonce, echostr, token: ", hashcode, signature, timestamp,
          nonce, echostr)
    if hashcode == signature:
        return echostr
    else:
        logging.warning("hashcode != signature")
        return ""





if __name__ == '__main__':
# app.debug = True

  #  app.run(host="0.0.0.0",port=5555,ssl_context=('2153883_xn--5vrwma.com.pem', '2153883_xn--5vrwma.com.key'))
    app.add_url_rule(rule='/myWerobot/', # WeRoBot 挂载地址
                 endpoint='werobot', # Flask 的 endpoint
                 view_func=make_view(myrobot),
                 methods=['GET', 'POST'])
    app.run(host="0.0.0.0",port=5555)
