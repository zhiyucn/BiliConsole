import requests
import login
import show_qrcode
import multiprocessing
import os
import time
import io
import werkzeug
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():    
    return send_file('qrcode.png', mimetype='image/png')

@app.route('/close')
def close():
    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()

def run_flask():
    app.run(host='0.0.0.0', port=2314)

import threading
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'  # 重置颜色
if os.path.exists("cookie.txt"):
    print(GREEN + "已登录" + RESET)
    Login = True
else:
    print(RED + "未登录" + RESET)
    Login = False
print(BLUE + "BiliConsole" + RESET)  
print(BLUE + "BiliConsole 正在加载..." + RESET)
from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests
def download_file(url, file_path, chunk_size=8192):
    from tqdm import tqdm
                
    try:
        # 获取文件总大小
        response = requests.head(url)
        total_size = int(response.headers.get('content-length', 0))
                
        # 创建进度条
        progress = tqdm(total=total_size, unit='B', unit_scale=True)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'https://www.bilibili.com/'
        }
        # 单线程下载
        response = requests.get(url, stream=True, headers=headers, cookies=json.loads(open("cookie.txt", "r").read()))
        response.raise_for_status()
                
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))
                    
        progress.close()
                
            
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise e
mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

def getMixinKey(orig: str):
    '对 imgKey 和 subKey 进行字符顺序打乱编码'
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    '为请求参数进行 wbi 签名'
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time                                   # 添加 wts 字段
    params = dict(sorted(params.items()))                       # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v 
        in params.items()
    }
    query = urllib.parse.urlencode(params)                      # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()    # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params

def getWbiKeys() -> tuple[str, str]:
    '获取最新的 img_key 和 sub_key'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Referer': 'https://www.bilibili.com/'
    }
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav', headers=headers)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key

img_key, sub_key = getWbiKeys()

print(BLUE + "BiliConsole 加载步骤1/1" + RESET)
# BiliConsole 字符画
print(f"""{BLUE}
██████╗ ██╗██╗     ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗
██╔══██╗██║██║     ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝
██████╔╝██║██║     ██║██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗ {RED} 
██╔══██╗██║██║     ██║██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝  
██████╔╝██║███████╗██║╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗
╚═════╝ ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝     {RESET}                                                                        
""")

print(GREEN + "Version: 1.0.0" + RESET)
print(RED + "请执行操作" + RESET)
if Login:
    print("1. 退出登录")
    print("2. 查看cookie")
    print("3. 查看登录状态")
    print("4. 获取用户信息")
    print("5. 看个视频")
    print("6. 退出")
else:
    print("1. 登录")
    print("2. 查看cookie")
    print("3. 查看登录状态")
    print("4. 获取用户信息")
    print("5. 看个视频")
    print("6. 退出")

while True:
    choice = input("请输入操作编号: ")
    if choice == "1":
        if Login:
            os.remove("cookie.txt")
            print(GREEN + "退出登录成功" + RESET)
            Login = False
        else:
            print(RED + "准备开始登录" + RESET)
            print(RED + "我们会给你2.5秒钟的时间准备扫码" + RESET)
            for i in range(250, 0, -1):
                print(f"倒计时: {i/100}秒", end="\r")
                time.sleep(0.01)
            temp = login.qrcode_login()
            if temp:
                print(GREEN + "登录成功" + RESET)
                Login = True
            else:
                print(RED + "登录失败" + RESET)
                Login = False
    elif choice == "2":
        if os.path.exists("cookie.txt"):
            with open("cookie.txt", "r") as f:
                print(f.read())
        else:
            print(RED + "cookie.txt文件不存在" + RESET)
    elif choice == "3":
        if os.path.exists("cookie.txt"):
            print(GREEN + "已登录" + RESET)
        else:
            print(RED + "未登录" + RESET)
    elif choice == "4":
        uid = input("请输入用户uid: ")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

        }
        print(RED + "正在获取用户信息" + RESET)
        if os.path.exists("cookie.txt"):
            print(GREEN + "开始进行WBI签名" + RESET)
            signed_params = encWbi(
                params={
                    'mid': uid,
                },
                img_key=img_key,
                sub_key=sub_key
            )
            query = urllib.parse.urlencode(signed_params)
            url = f"https://api.bilibili.com/x/space/wbi/acc/info?{query}"
            import json
            response = requests.get(url, headers=headers, cookies=json.loads(open("cookie.txt", "r").read()))
            
        else:
            print(RED + "cookie.txt文件不存在" + RESET)
            print(RED + "此API需要登陆" + RESET)
            print(RED + "或者使用旧版API（有请求次数限制）" + RESET)
            print(RED + "是否使用旧版API？(Y/n)" + RESET)
            choice = input()
            if choice == "Y" or choice == "y":
                print(RED + "正在使用旧版API" + RESET)
                url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
                response = requests.get(url, headers=headers)
        
        data = response.json()
        print("正在整理数据...")
        if data["code"] == 0:
            name = data["data"]["name"]
            face = data["data"]["face"]
            sex = data["data"]["sex"]
            level = "Lv." + str(data["data"]["level"])
            print(GREEN + "获取成功" + RESET)
            print("用户信息:")
            print(f"用户名: {name}")
            print(f"头像图片链接: {face}")
            print(f"性别: {sex}")
            print(f"等级: {level}")
            print("是否生成个人信息表（图片）？(Y/n)")
            choice = input()
            if choice == "Y" or choice == "y":
                print("正在生成个人信息表...")
                print("获取API2...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                }
                response = requests.get(f"https://api.bilibili.com/x/web-interface/card?mid={uid}", headers=headers, cookies=json.loads(open("cookie.txt", "r").read()))
                data2 = response.json()
                from PIL import Image, ImageDraw, ImageFont, ImageFilter
                # 创建一个空白的图片
                img = Image.new('RGB', (800, 800), color = (255, 255, 255))
                # 下载头像
                response = requests.get(face)
                avatar = Image.open(io.BytesIO(response.content))
                # 调整头像大小并添加圆形蒙版
                avatar = avatar.convert('RGBA')
                avatar = avatar.resize((150, 150))
                mask = Image.new('L', (150, 150), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, 150, 150), fill=255)
                avatar.putalpha(mask)
                
                # 将头像粘贴到图片上
                img.paste(avatar, (325, 50), avatar)
                
                # 创建一个画笔
                draw = ImageDraw.Draw(img)
                
                # 设置字体
                title_font = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', 28)
                info_font = ImageFont.truetype('C:\\Windows\\Fonts\\msyh.ttc', 20)
                
                # 绘制标题
                draw.text((400, 220), f"{name}", fill=(0, 0, 0), font=title_font, anchor='mm')
                
                # 绘制基本信息
                draw.text((100, 280), f"性别: {sex}", fill=(0, 0, 0), font=info_font)
                draw.text((100, 310), f"等级: {level}", fill=(0, 0, 0), font=info_font)
                
                fans = data2['data']['card']['fans']
                draw.text((100, 340), f"粉丝数: {fans}", fill=(0, 0, 0), font=info_font)

                sign = data2['data']['card']['sign']
                draw.text((100, 370), f"签名: {sign}", fill=(0, 0, 0), font=info_font)
                

                
                # 添加装饰线
                draw.line([(50, 260), (750, 260)], fill=(200, 200, 200), width=2)
                
                # 最底部
                draw.text((400, 750), f"Powered by BiliConsole", fill=(0, 0, 0), font=info_font)
                draw.text((400, 780), f"Version: 1.0.0", fill=(0, 0, 0), font=info_font)
                draw.text((400, 810), f"MIT License", fill=(0, 0, 0), font=info_font)
                # 保存图片
                img.save('user_info.png')
                print(GREEN + "个人信息表已生成" + RESET)
            else:
                print(RED + "已取消" + RESET)
        else:
            print(RED + "获取失败" + RESET)
            print(f"错误信息: {data['message']}")
    elif choice == "5":
        av = input("请输入av或bv号: ")
        print("正在获取视频信息...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': f"https://www.bilibili.com/video/{av}"
        }
        if av.startswith("BV"):
            print("检测到BV号，正在转换为AV号...")
            av = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={av}", headers=headers).json()["data"]["aid"]
            print(f"AV号: {av}")
        print("开始获取cid Step 1")
        #if av.startswith("BV"):
        #    response = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={av}",headers=headers)
        #else:
        response = requests.get(f"https://api.bilibili.com/x/web-interface/view?aid={av}", headers=headers)
        data = response.json()
        if 'data' not in data or 'cid' not in data['data']:
            print(f"{RED}获取视频信息失败: {data.get('message', '未知错误')}{RESET}")
        #if av.startswith("BV"):
        #    cid = data['data']['cid']
        #    av = data['data']['aid']
        cid = data['data']['cid']
        print("开始获取链接 Step 2")
        play_url = requests.get(f"https://api.bilibili.com/x/player/playurl?avid={av}&cid={cid}", headers=headers).json()["data"]["durl"][0]["url"]
        print("开始下载 Step 3")
        download_file(play_url, f"{av}.mp4")