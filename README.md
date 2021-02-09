五维学子领水脚本，你还在苦恼早上起来打水时尴尬的“嘀~~”的一声吗？还在苦恼今天又忘记领取补贴了吗？这种活还是交给计算机来做吧 : ) 能偷懒的绝不动手 : )
## 登录方式
- 身份证（不推荐）
- 手机登录（推荐）
- 学号登录（最推荐）

但从软件给出的信息中，学号登录只适用几所学校，所以手机登录是比较好的选择。

软件的默认密码是身份证后6位（建议先修改密码再使用该脚本）
## 修改信息
以下操作均在个人中心操作

打开APP--->底部导航栏找到个人中心--->点击进入
### 绑定手机号
在上述位置找到手机绑定--->依照提示完成绑定
### 修改密码
在上述位置点击自己的头像--->看到最后的账号密码--->依照提示完成更改
## 使用
首先在school_code.json里面找到自己的学校，然后在user.json中填入相关信息

### user.json
#### 参数说明
| 参数         | 类型   | 说明       | 必填 |
| ------------ | ------ | ---------- | ---- |
| id_number    | string | 身份证号码 | 选填 |
| phone_number | string | 手机号     | 选填 |
| student_id   | string | 学号       | 选填 |
| passwd       | string | 密码       | 必填 |
| school_code  | string | 学校代码   | 必填 |

#### 示例
```json
[
    {
        "id_number": "xxxxxx",
        "passwd": "xxxxx",
        "school_code": "10"
    },
    {
        "student_id":"xxxxx",
        "passwd": "xxxxx",
        "school_code": "10"
    },
        {
        "phone_number":"xxxxxxxxxxx",
        "passwd": "xxxxx",
        "school_code": "10"
    },
]
```
## 推送消息
使用了Server酱 你可以到Server酱的官网申请一个ID然后填入`main.py`的`SERVER_CHAN_KEY = ''`里面去

或者默认打印在console中

## 后续
有空考虑加一个交互的脚本或者界面来填写上述的`填起来有点麻烦`的必填信息