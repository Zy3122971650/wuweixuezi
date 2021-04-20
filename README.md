# 五维学子领水脚本
啊！亲爱的同学，你还在为每天早上忘记打开五维学子领取0.7元的热水补助而在热水器面前听到di的一声而苦恼吗？来吧！使用它，~~懒惰起来~~解放自己的心智负担。

如果你**信任**我的话，可以使用我已经部署好的项目，一键懒惰。所收集到的数据仅用于自动领水。[--->传送门<---](https://wuweixuezi.iseelntu.com)

## 目录结构

```bash
.
├── main
│   ├── backend.py
│   ├── core.py
│   ├── cron_scrip.py
│   ├── gunicorn.conf.py
│   └── __pycache__
│       └── core.cpython-39.pyc
├── README.md
└── vue
    └── app
        ├── babel.config.js
        ├── dist
        ├── node_modules
        ├── package.json
        ├── public
        ├── README.md
        ├── src
        ├── vue.config.js
        └── yarn.lock
```

### main
1. 由flask编写的网站后端`backend.py`，用于验证由前端传来的账号和密码，然后存入数据库。
2. gunicorn的配置文件`gunicorn.conf.py`，项目使用gunicorn部署flask
3. `cron_scrip.py`是签到脚本，你可以使用cron或者编写systemd服务和定时器。
4. `core.py`包括两个类，一个是关于五维学子的类，包括登录和验证账户等方法；另一个是关于dynamodb的数据库读写操作。

### vue
这是一个标准的由Vue CLI构建的Vue项目。

## 使用教程
为了白嫖亚马逊的免费数据库，我使用了dynamodb作为我的数据库。（很草率是吧，主要是嫌服务器到期之后数据迁移起来麻烦）如果你有空编写使用其他数据库的版本，可以参照[完善项目](#完善项目)

以下以网页作为录入数据进入数据库的入口，以亚马逊dynamodb作为数据库为例讲解使用方法。

### Clone
登录到你的服务器克隆项目：`git clone https://github.com/Zy3122971650/wuweixuezi.git`
### 安装依赖
安装python依赖
```bash
python3 -m pip install requirements.txt
```
安装yarn

[Yarn官方文档](https://yarn.bootcss.com/docs/install/#debian-stable)

补全Vue项目中的依赖
```bash
cd vue/app
yarn
```

### 补全脚本参数
见`cron_scrip.py`
```python
wuweixuezi = core.wuweixuezi(server_chan_key=None)
db = core.dynamodb(region_name=None, aws_access_key_id=None,
                       aws_secret_access_key=None)

```
我们使用了ServerChan来推送消息，以监控服务有没有按时工作。如果你也需要的话，参见[Server酱官网](https://sct.ftqq.com/)，把你的`SendKey`填入`server_chan_key`。

见`backend.py`
```python
db = core.dynamodb(region_name=None, aws_access_key_id=None,
                       aws_secret_access_key=None)

```
`region_name`是你使用的dynamodb数据库所在的区，`aws_access_key_id和aws_secret_access_key`你需要在亚马逊的`IAM`服务里申请。

### 部署
#### 构建网页
```bash
cd vue/app
yarn build
```

#### 部署flask服务器

flask后端不要直接用`python3 backend.py`运行，我们使用用法简单的gunicorn部署flask在后台守护运行，端口是配置文件所配置的`4000`。
```bash
cd main
python3 -m gunicorn backend:app -c gunicorn.conf.py --daemon
``` 

### 部署网页
由于后端是和前端分离的，我们需要在部署网页的时候设置反向代理。我们需要把前端发出的`http(s)://example.com/api/save`反向代理到`http://127.0.0.1/save`（127.0.0.1参见gunicorn的配置）

如果你要把网站放在不安全的位置，你可能还需要配置SSL

### nginx的参考配置
我使用的是nginx，在这里举个例子。
![20210419233949](https://i.loli.net/2021/04/19/C83c2VHSobIzu6E.png)
## 完善项目
项目还不具备一键部署的能力，也不具备支持多种数据库的能力。如果你希望支持多一种数据库你可以参与到项目中来。虽然我也是一个新手，对github和git的使用还不熟练，但我希望我们可以在这个项目中共同进步。

### 添加新的数据库
你只需在`core.py`中添加一个新的类，你需要至少需要实现`check_user`、`read_all_user_info`、`set_item`三大功能。

| 函数               | 参数 | 用途                                                               | 返回值                         |
| ------------------ | ---- | ------------------------------------------------------------------ | ------------------------------ |
| check_user         | id   | 通过用户ID判断，该用户是否重复添加                                 | 用户已经存在返回1，不存在返回0 |
| read_all_user_info | None | 读取所有用户的信息                                                 | 元素是单个用户信息的列表       |
| set_item           | data | data是前端返回的所有登录信息的集合，把data中的信息全部存入数据库中 | None                           |

### 提Issue
如果你对本项目有什么想法，可以提Issue。在时间允许的情况下我会进行跟进。