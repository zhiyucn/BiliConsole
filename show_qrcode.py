from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
import os
app = Flask(__name__)

@app.route('/')
def index():    
    return send_file('qrcode.png', mimetype='image/png')

@app.route('/close')
def close():
    # 获取自己PID
    pid = os.getpid()
    # 关闭自己
    os.kill(pid, 9)
def run(port=2314):
    app.run(host='0.0.0.0', port=port)

def render_qr_code(qr_str):
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # 保存二维码到文件
    img.save("qrcode.png")
