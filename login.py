import show_qrcode
import requests
import json
import time
import os
import multiprocessing
def qrcode_login():
    #try:
        #flask = multiprocessing.Process(target=show_qrcode.run)
        #flask.start()
    #except Exception as e:
        #print(f"Flask服务器启动失败: {e}")
        #return False
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://passport.bilibili.com/',
    }
    response = requests.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate", headers=headers)
    data = json.loads(response.text)
    qr_str = data["data"]["url"]
    show_qrcode.render_qr_code(qr_str)
    key = data["data"]["qrcode_key"]
    print("请使用哔哩哔哩APP扫描二维码登录")
    os.system("start http://127.0.0.1:2314/")
    test_count = 0
    while True:
        test_count += 1
        if test_count > 180:  # 超过3分钟，退出循环
            print("二维码已过期，请重新运行程序")
            return False
            
        url = f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={key}"
        response = requests.get(url, headers=headers)
        res = response
        response = json.loads(response.text)
        if response["data"]["code"] == 0:
            print(f"在{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}登录成功！")
            requests.get("http://127.0.0.1:2314/close")
            cookie = res.cookies.get_dict()
            print(cookie)
            with open("cookie.txt", "w") as f:
                f.write(json.dumps(cookie))
            print("cookie已保存到cookie.txt文件中")
            return True
        else:
            print(f"在{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}登录失败！")
            print(f"错误信息：{response['message']}")
        time.sleep(4)
if __name__ == '__main__':
    qrcode_login()