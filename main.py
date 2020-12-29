import time
import hashlib
import json
import requests

headers_UA = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'
}
headers_com = {
    'X-Requested-With': 'com.r13760640363.eig',
    'Accept-Encoding': 'gzip, deflate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script'
}

nick_name = ''
token = ""
log = ""
r = ""
SERVER_CHAN_KEY = 'https://sc.ftqq.com/SCU121621Tc8fee35f7b29cb69bf08961d7a713b805f9a716c257d9.send'


def server_chan():
    global log
    data = {
        'text': "水卡的信息哟！",
        'desp': log
    }
    requests.post(
        SERVER_CHAN_KEY, data=data)


def printf(msg):
    if not SERVER_CHAN_KEY:
        print(msg)


def save_data(user_info):
    with open("user.json", 'w+') as f:
        f.write(json.dumps(user_info, indent=4))
    pass


def load_data():
    import os
    if os.path.exists("user.json"):
        with open("user.json", 'r') as f:
            data = f.read()
        return 1, json.loads(data)
    return 0, None


def set_token_and_nickname(school_code, user_name, passwd):
    global nick_name, token
    sign, time_ = get_sign_time()
    url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.login&jsoncallback=1&time={time}&sign={sign}&style=1&schoolID={school}&identityID={id}&realname=&studentID=&mobile=&password={passwd}&wxUserToken=&_={time}"
    url = url.format(sign=sign, school=school_code, time=time_,
                     id=user_name, passwd=passwd)
    response = r.get(url, headers=headers_com.update(headers_UA))
    nick_name = json.loads(response.text[2:-1])['errmsg']['nickname']
    token = json.loads(response.text[2:-1])['errmsg']['token']


def set_cookies():
    sign, time_ = get_sign_time()
    url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.setCookie&jsoncallback=1&time={time}&sign={sign}&token={token}&_={time}"
    url = url.format(time=time_, sign=sign, token=token)

    r.get(url, headers=headers_com.update(headers_UA))


def set_device():
    sign, time_ = get_sign_time()
    url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.setDeviceid&jsoncallback=jQuery17200070308321888847836_1609130595155&time={time}&sign={sign}&token={token}&deviceid=100d855909fb7555aaa&deviceType=Mi+10&_={time}"
    url = url.format(sign=sign, time=time_, token=token)
    r.get(url, headers=headers_com.update(headers_UA))


def get_sign_time():
    m = hashlib.md5()
    date = int(time.time())
    data = str(date*4)+"Water#$@2017"
    data = data.encode(encoding="utf-8")
    m.update(data)
    return m.hexdigest(), str(date)


def sign_in():
    global log
    url = 'http://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&op=ajaxsign&do=my_integral&m=water'
    Headers = {
        'Host': 'www.wuweixuezi.com',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Accept': 'text/html, */*; q=0.01',
        'Origin': 'http://www.wuweixuezi.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.wuweixuezi.com/app/index.php?i=2&c=entry&do=my_integral&m=water&winName=index&frameName=frame0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = r.post(
        url, headers=Headers.update(headers_UA))
    if "已经签到" in response.text:
        log += '\n- [x] 签到'
        printf("已经签到")
    elif 'APP' in response.text:
        log += '\n- [ ] 签到 (请使用APP)'
        printf("使用APP")
    elif '签到' in response.text:
        log += '\n- [x] 签到'
    else:
        log += '\n- [ ] 签到（未知错误）'


def water():
    global log
    sign, time_ = get_sign_time()
    url = 'https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.leadSpea&jsoncallback=1&time={time}&sign={sign}&token={token}&type=1&_{time}'
    url = url.format(sign=sign, time=time_, token=token)
    response = r.get(
        url, headers=headers_com.update(headers_UA))
    if '已经领取' == json.loads(response.text[2:-1])["errmsg"]:
        log += '\n- [x] 领取0.7热水'
    printf(json.loads(response.text[2:-1])["errmsg"])


def main():
    global r, log
    status, user_info = load_data()
    if not status:
        print("请补全user.json中空缺内容")
        exit(1)
    for index in user_info.keys():
        print('{}/{}'.format(int(index)+1, len(user_info.keys())), end='\r')
        r = requests.session()
        user_name = user_info[index]["user_name"]
        passwd = user_info[index]["passwd"]
        school_code = user_info[index]["school_code"]
        set_token_and_nickname(school_code, user_name, passwd)
        printf(nick_name)
        log += '\n###'+nick_name
        set_cookies()
        set_device()
        sign_in()
        water()
    server_chan()
    pass


main()
