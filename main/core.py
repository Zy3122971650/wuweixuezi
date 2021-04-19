import hashlib
import json
import sys
import time

import boto3
from boto3.dynamodb.conditions import Key
import requests


class wuweixuezi(object):
    def __init__(self, server_chan_key=None):
        self.SERVER_CHAN_KEY = server_chan_key
        self.HEADERS_UA = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'
        }
        self.HEADERS_COM = {
            'X-Requested-With': 'com.r13760640363.eig',
            'Accept-Encoding': 'gzip, deflate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script'
        }
        self.r = requests.session()
        self.token = ''

    def _generate_time_sign(self):
        m = hashlib.md5()
        date = int(time.time())
        data = str(date*4)+"Water#$@2017"
        data = data.encode(encoding="utf-8")
        m.update(data)
        return m.hexdigest(), str(date)

    def _login_base(self, id_number=None, phone_number=None, password=None, school_code=None, style=None):
        sign, time_ = self._generate_time_sign()
        url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.login&jsoncallback=1&time={time}&sign={sign}&style={style}&schoolID={school}&identityID={id_number}&realname=&studentID={student_id}&mobile={phone_number}&password={passwd}&wxUserToken=&_={time}"
        url = url.format(sign=sign, school=school_code, time=time_,
                         passwd=password, id_number=id_number, phone_number=phone_number, student_id='', style=style)

        response = self.r.get(
            url, headers=self.HEADERS_COM.update(self.HEADERS_UA))
        response = json.loads(response.text[2:-1])
        return response

    def get_user_base_info(self, id_number=None, phone_number=None, password=None, school_code=None, style=None):
        return self._login_base(
            id_number, phone_number, password, school_code, style)['errmsg']

    def check_login_params(self, id_number=None, phone_number=None, password=None, school_code=None, style=None):
        data = self._login_base(
            id_number, phone_number, password, school_code, style)
        if data['errcode'] != '0':
            return 0
        else:
            return 1

    def _get_token(self, id_number=None, phone_number=None, password=None, school_code=None, style=None):
        data = self._login_base(
            id_number, phone_number, password, school_code, style)
        self.token = data['errmsg']['token']

    def _set_cookies(self):
        sign, _time = self._generate_time_sign()
        url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.setCookie&jsoncallback=1&time={time}&sign={sign}&token={token}&_={time}"
        url = url.format(time=_time, sign=sign, token=self.token)
        self.r.get(url, headers=self.HEADERS_COM.update(self.HEADERS_UA))

    def _set_device(self):
        sign, _time = self._generate_time_sign()
        url = "https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.setDeviceid&jsoncallback=jQuery17200070308321888847836_1609130595155&time={time}&sign={sign}&token={token}&deviceid=100d855909fb7555aaa&deviceType=Mi+10&_={time}"
        url = url.format(time=_time, sign=sign, token=self.token)
        self.r.get(url, headers=self.HEADERS_COM.update(self.HEADERS_UA))

    def _sign_in(self):
        url = 'http://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&op=ajaxsign&do=my_integral&m=water'
        headers = {
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
        self.r.post(url, headers=headers.update(self.HEADERS_UA))

    def _receive_water(self):
        sign, _time = self._generate_time_sign()
        url = 'https://www.wuweixuezi.com/app/index.php?i=2&j=3&c=entry&m=water&do=appapi&op=user.leadSpea&jsoncallback=1&time={time}&sign={sign}&token={token}&type=1&_{time}'
        url = url.format(sign=sign, time=_time, token=self.token)
        self.r.get(url, headers=self.HEADERS_COM.update(self.HEADERS_UA))

    def server_chan(self, count):
        server_url = 'https://sctapi.ftqq.com/{}.send'.format(
            self.SERVER_CHAN_KEY)
        data = {
            'text': "水卡程序的日记哟！",
            'desp': '完成领水任务，共{}个账户'.format(count)
        }
        requests.post(
            server_url, data=data)

    def _clean(self):
        self.r = requests.session()
        self.token = ''

    def task_start(self, id_number=None, phone_number=None, password=None, school_code=None, style=None):
        self._get_token(id_number, phone_number, password, school_code, style)
        self._set_cookies()
        self._set_device()
        self._sign_in()
        self._receive_water()
        self._clean()


class dynamodb(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name,
                                       aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def init_database(self):
        self.dynamodb.create_table(TableName='wuweixuezi',
                                   KeySchema=[
                                       {'AttributeName': 'type', 'KeyType': 'HASH'}, {'AttributeName': 'id', 'KeyType': 'RANGE'}],
                                   AttributeDefinitions=[
                                       {
                                           'AttributeName': 'type',
                                           'AttributeType': 'N',
                                       },
                                       {
                                           'AttributeName': 'id',
                                           'AttributeType': 'S',
                                       }, ],
                                   ProvisionedThroughput={
                                       'ReadCapacityUnits': 5,
                                       'WriteCapacityUnits': 5
                                   })

    def set_item(self, data):
        table = self.dynamodb.Table('wuweixuezi')
        table.put_item(Item=data)

    def _read_all_user_base(self, type):
        table = self.dynamodb.Table('wuweixuezi')
        raw_datas = table.query(
            KeyConditionExpression=Key('type').eq(type))['Items']
        return [raw_data['info'] for raw_data in raw_datas]

    def _read_all_id_card_user(self):
        return self._read_all_user_base(1)

    def _read_all_phone_number_user(self):
        return self._read_all_user_base(3)

    def read_all_user_info(self):
        return self._read_all_id_card_user()+self._read_all_phone_number_user()

    def check_user(self, id):
        table = self.dynamodb.Table('wuweixuezi')
        # try:
        response = table.query(KeyConditionExpression=Key(
            'type').eq(1) & Key('id').eq(id))
        if response['Count'] == 0:
            response = table.query(KeyConditionExpression=Key(
                'type').eq(3) & Key('id').eq(id))
            if response['Count'] == 0:
                return 0
        return 1
