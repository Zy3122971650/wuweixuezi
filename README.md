目前只支持用身份证登录，其他登录方法没注意弄，懒得搞了
## 使用
首先在school_code.json里面找到自己的学校，然后在user.json中填入相关信息

举个例子：（以两个人为例）

比如说两个人都是辽宁工程技术大学葫芦岛校区的，那么在school_code里面找，就是10。
然后在user.json里面填

其中，`user_name`就是你的身份证号码 `passwd`一般没改就是身份证后6位,`school_code`就是刚刚找的10
```json
[
    {
        "user_name": "xxxxxx",
        "passwd": "xxxxx",
        "school_code": "10"
    },
    {
        "user_name": "xxxxxx",
        "passwd": "xxxxx",
        "school_code": "10"

    }
]
```

## 后续
有空考虑加一个交互的脚本或者界面来填写上述的`填起来有点麻烦`的必填信息