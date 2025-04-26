
import qrcode
from io import BytesIO
import os

def render_qr_code(qr_str):
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # 保存二维码到文件
    img.save("qrcode.png")
