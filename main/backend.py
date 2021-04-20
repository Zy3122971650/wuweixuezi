import core
from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)

CORS(app)


def set_error(error, code, messg):
    error['code'] = code
    error['messg'] = messg
    return error


@app.route('/save', methods=['POST'])
def save():
    error = {'code': '', 'messg': ''}
    wuweixuezi = core.wuweixuezi()
    data = request.json['data']
    # 处理空格
    for key in data.keys():
        if key == 'style':
            continue  # 它不是字符串类型
        data[key] = data[key].strip(' ')
    user_invalid_flag = wuweixuezi.check_login_params(
        data['id_number'], data['phone_number'], data['password'], data['school_code'], data['style'])
    if user_invalid_flag == 0:
        error = set_error(error, '1', '哎！账号或者密码记错了呢（身份证中的x是小写哦！）')
        return error

    user_info = wuweixuezi.get_user_base_info(
        data['id_number'], data['phone_number'], data['password'], data['school_code'], data['style'])
    user_id = user_info['id']

    db = core.dynamodb(region_name=None, aws_access_key_id=None,
                       aws_secret_access_key=None)

    user_is_exist_flag = db.check_user(user_id)
    if user_is_exist_flag == 1:
        error = set_error(error, '2', '不要重复添加账号嗷，小张已为你驳回请求')
        return error
    db.set_item({'type': data['style'], 'id': user_id, 'info': data})
    return set_error(error, '0', '小张会记得每天为你领水的')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
