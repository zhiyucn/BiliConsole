from PIL import Image
import qrcode
import io
import sys

def generate_qr_code(content):
    """
    从文本或URL生成二维码图像
    :param content: 要编码的文本或URL
    :return: PIL图像对象
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def qr_to_string(image_path_or_content):
    """
    将二维码图像或文本内容转换为字符串表示
    :param image_path_or_content: 二维码图片路径或要编码的文本/URL
    :return: 字符串形式的二维码
    """
    img = Image.open(image_path_or_content).convert('1')  # 转换为黑白图像
    width, height = img.size
    
    # 使用■表示黑色像素，□表示白色像素
    result = []
    # 动态计算采样步长，保持宽高比
    step_y = max(1, height // 50)  # 高度方向步长
    step_x = max(1, width // 100)   # 宽度方向步长，增加采样密度
    for y in range(0, height, step_y):
        line = []
        for x in range(0, width, step_x):
            pixel = img.getpixel((x, y))
            line.append('█' if pixel == 0 else ' ')
        result.append(''.join(line))
    
    return '\n'.join(result)

def render_qr_code(qr_str):
    input_content = qr_str
# 如果是URL或文本则生成二维码，否则检查是否是文件路径
    if input_content.startswith(('http://', 'https://')) or len(input_content.split()) > 1:
        img = generate_qr_code(input_content)
        # 保存二维码图像到文件
        img.save('qr_code.png')
        # 将二维码图像保存到内存中
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        qr_str = qr_to_string(img_bytes)
    else:
        # 检查是否是有效的文件路径
        try:
            with open(input_content, 'rb') as f:
                qr_str = qr_to_string(input_content)
        except (FileNotFoundError, IOError):
            # 如果不是文件，则作为文本内容生成二维码
            img = generate_qr_code(input_content)
            img.save('qr_code.png')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            qr_str = qr_to_string(img_bytes)
    
    print(qr_str)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python qr_to_string.py <二维码图片路径或文本内容>")
        sys.exit(1)
    
    input_content = sys.argv[1]
    
    # 如果是URL或文本则生成二维码，否则检查是否是文件路径
    if input_content.startswith(('http://', 'https://')) or len(input_content.split()) > 1:
        img = generate_qr_code(input_content)
        # 保存二维码图像到文件
        img.save('qr_code.png')
        print(f"二维码已生成并保存为qr_code.png，请确认后再继续")
        input("按Enter键继续转换为字符串...")
        # 将二维码图像保存到内存中
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        qr_str = qr_to_string(img_bytes)
    else:
        # 检查是否是有效的文件路径
        try:
            with open(input_content, 'rb') as f:
                qr_str = qr_to_string(input_content)
        except (FileNotFoundError, IOError):
            # 如果不是文件，则作为文本内容生成二维码
            img = generate_qr_code(input_content)
            img.save('qr_code.png')
            print(f"二维码已生成并保存为qr_code.png，请确认后再继续")
            input("按Enter键继续转换为字符串...")
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            qr_str = qr_to_string(img_bytes)
    
    print(qr_str)