#### 登录注册功能

- 不设置，任何人可查询价格曲线以及实现预测
- 设置，任何人可查询价格曲线，但只有注册登录的人能够查询预测价格
- 预测价格就设置为接下来的10天左右，把预测值曲线列出来即可

#### 爬虫

- 每天定时爬取71种蔬菜的价格，存放至mongodb
- 数据库

#### 模型预测：

- ARIMA：直接用所有数据进行预测
- bp：用训练好的模型，将最新的数据的100个导入进行预测
- lstm：同上

- bp和lstm可每隔半年重新训练一次

#### 语言和技术：

- tensorflow
- python的flask开发后台
- 部署：使用docker-compose部署，redis，mongodb，python各自的镜像结合起来

#### 接口

##### 1. 用户接口

- 1.1 注册：/user/register
- 1.2 登录：/user/login
- 1.3 修改密码：/user/alter_pwd
- 1.4 获取模型信息：/user/model/information
- 1.5 选择模型进行预测：/user/model/predict
- 1.6 查询蔬菜价格曲线：/user/vegetable/k_line
- 1.7 查询蔬菜信息：/user/vegetable/information

##### 2. 管理员接口

- 2.1 管理员增删系统的蔬菜种类：/master/alter_vegetable
- 2.2 管理员禁用用户：/master/ban_user
- 2.3 管理员删除用户：/master/delete_user
- 2.4 管理员进行某种蔬菜模型的训练：/master/train_model

##### 3. 超级管理员接口

- 3.1 超级管理员从用户中添加管理员：/root/add_master
- 3.2 超级管理员删除管理员：/root/delete_master

#### 具体实现

##### 1.1 注册API

###### 简要描述

- 用户注册

###### 请求URL

- /user/register

请求方式

- POST

###### 参数

|   参数名   | 必选 |  类型  |    说明    |
| :--------: | :--: | :----: | :--------: |
| user_name  |  是  | string |   用户名   |
|  password  |  是  | string |  用户密码  |
|   email    |  是  | string |  电子邮箱  |
| email_code |  是  | string | 邮箱验证码 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully"
}
```



##### 1.2 登录API

###### 简要描述

- 用户、管理员登录

###### 请求URL

- /user/login

请求方式

- POST

###### 参数

|  参数名   | 必选 |  类型  |   说明   |
| :-------: | :--: | :----: | :------: |
| user_name |  是  | string |  用户名  |
| password  |  是  | string | 用户密码 |
|   code    |  是  | string |  验证码  |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully"
}
```



##### 1.3 修改密码API

###### 简要描述

- 用户修改密码

###### 请求URL

- /user/alter_pwd

请求方式

- POST

###### 参数

|    参数名    | 必选 |  类型   |     说明     |
| :----------: | :--: | :-----: | :----------: |
|  user_name   |  是  | string' |    用户名    |
| new_password |  是  | string  |   用户密码   |
| re_password  |  是  | string  | 重新输入密码 |
|    email     |  是  | string  |   电子邮箱   |
|  email_code  |  是  | string  |  邮箱验证码  |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully"
}
```



##### 1.4 获取模型信息API

###### 简要描述

- 获取模型信息

###### 请求URL

- /user/model/information

请求方式

- GET

###### 参数

- 无

###### 返回示例

```json
{
    "code": 200,
    "msg": "successfully",
    "data": {
        "name": ["ARIMA模型", "BP神经网络模型", "LSTM神经网络模型"],
        "msg": ["误差在1%以内准确率30%，5%以内准确率40%， 10%以内准确率50%", "误差在1%以内准确率30%，5%以内准确率40%， 10%以内准确率50%", "误差在1%以内准确率30%，5%以内准确率40%， 10%以内准确率50%"]
    }
}
```

###### 返回参数说明

| 参数名 |  类型  |     说明     |
| :----: | :----: | :----------: |
|  code  |  int   | 请求结果代码 |
|  msg   | string | 操作结果说明 |
|  data  |  json  | 请求结果数据 |

###### data参数字段说明

| 字段名 |     类型      |      说明      |
| :----: | :-----------: | :------------: |
|  name  | list & string |     模型名     |
|  msg   | list & string | 对应模型说明等 |





##### 1.5 模型预测API

###### 简要描述

- 选择某个模型进行价格的预测

###### 请求URL

- /user/model/predict

请求方式

- POST

###### 参数

|     参数名     | 必选 |     类型      |          说明          |
| :------------: | :--: | :-----------: | :--------------------: |
|   model_name   |  是  |    string     | 模型名，或是模型的标识 |
| vegetable_name |  是  |    string     | 蔬菜名，或是蔬菜的标识 |
|      date      |  是  | list & string |    已有蔬菜价格日期    |
|      days      |  是  |      int      |      欲预测的天数      |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully", 
    "data": {
        "date": ["2018-01-01", "2018-01-02", ... , "2019-03-01"],
        "price": [11.1, 11.1 , ... , 11.1]
    }
}
```

###### data参数字段说明

| 字段名 |     类型      |                 说明                 |
| :----: | :-----------: | :----------------------------------: |
|  date  | list & string | 传入蔬菜价格日期加上预测的天数的日期 |
| price  | list & float  |    传入蔬菜价格加上预测天数的价格    |





##### 1.6 查询蔬菜价格曲线API

###### 简要描述

- 查询蔬菜价格曲线

###### 请求URL

- /vegetable/k_line

请求方式

- POST

###### 参数

|     参数名     | 必选 |     类型      |            说明            |
| :------------: | :--: | :-----------: | :------------------------: |
| vegetable_name |  是  | list & string | 多个蔬菜名，或是蔬菜的标识 |
|      date      |  是  | list & string |      已有蔬菜价格日期      |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully", 
    "data": {
        "vegetable_name": ["大白菜", "小白菜"],
        "date": ["2018-01-01", "2018-01-02", ... , "2019-03-01"],
        "price": [[11.1, 11.1 , ... , 11.1], [22.2, 22.2 , ..., 22.2]]
    }
}
```

###### data参数字段说明

|     字段名     |        类型         |                 说明                 |
| :------------: | :-----------------: | :----------------------------------: |
| vegetable_name |    list & string    |          一个或者多个蔬菜名          |
|      date      |    list & string    | 传入蔬菜价格日期加上预测的天数的日期 |
|     price      | list & list & float |         蔬菜在日期区间内价格         |



##### 1.7 查询蔬菜信息API

###### 简要描述

- 查询蔬菜信息

###### 请求URL

- /vegetable/information

请求方式

- POST

###### 参数

|     参数名     | 必选 |     类型      |            说明            |
| :------------: | :--: | :-----------: | :------------------------: |
| vegetable_name |  是  | list & string | 多个蔬菜名，或是蔬菜的标识 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "successfully", 
    "data": {
        "msg":"xxx是一种生长在冬天的植物"
    }
}
```

###### data参数字段说明

| 字段名 |  类型  |        说明        |
| :----: | :----: | :----------------: |
|  msg   | string | 对该蔬菜的信息介绍 |



##### 2.1 增删蔬菜种类API

###### 简要描述

- 管理员增删系统的蔬菜种类（前端应该设计地成为列出可选择项，即江南市场拥有的蔬菜）

###### 请求URL

- /master/alter_vegetable

请求方式

- POST

###### 参数

|     参数名     | 必选 |     类型      |    说明    |
| :------------: | :--: | :-----------: | :--------: |
| vegetable_name |  是  | list & string | 多个蔬菜名 |
|  operate_type  |  是  |    boolean    |   增/删    |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "alter successfully", 
}
```



##### 2.2 禁用用户API

###### 简要描述

- 管理员禁用用户

###### 请求URL

- /master/ban_user

请求方式

- POST

###### 参数

|  参数名   | 必选 |  类型  |  说明  |
| :-------: | :--: | :----: | :----: |
| user_name |  是  | string | 用户名 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "ban successfully", 
}
```



##### 2.3 删除用户API

###### 简要描述

- 管理员删除用户

###### 请求URL

- /master/delete_user

请求方式

- POST

###### 参数

|  参数名   | 必选 |  类型  |  说明  |
| :-------: | :--: | :----: | :----: |
| user_name |  是  | string | 用户名 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "delete successfully", 
}
```



##### 2.4 进行某种蔬菜模型的训练API

###### 简要描述

- 管理员进行某种蔬菜模型的训练

###### 请求URL

- /master/train_model

请求方式

- POST

###### 参数

|   参数名   | 必选 |  类型  |  说明  |
| :--------: | :--: | :----: | :----: |
| model_name |  是  | string | 用户名 |
|  veg_name  |  是  | string | 蔬菜名 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "start to train", 
}
```



##### 3.1 添加管理员API

###### 简要描述

- 超级管理员从用户中添加管理员

###### 请求URL

- /root/add_master

请求方式

- POST

###### 参数

|  参数名   | 必选 |  类型  |  说明  |
| :-------: | :--: | :----: | :----: |
| user_name |  是  | string | 用户名 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "add seccessfully", 
}
```



##### 3.1 删除管理员API

###### 简要描述

- 超级管理员删除管理员

###### 请求URL

- /root/delete_master

请求方式

- POST

###### 参数

|  参数名   | 必选 |  类型  |  说明  |
| :-------: | :--: | :----: | :----: |
| user_name |  是  | string | 用户名 |

###### 返回示例

```json
{
    "code": 200, 
    "msg": "delete seccessfully", 
}
```



