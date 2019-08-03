#### 登录注册功能

- 设置，但只有注册登录的人能够查询预测价格
- 预测价格就设置为接下来的10天左右，把预测值曲线列出来即可

#### 爬虫

- 每天定时爬取71种蔬菜的价格，存放至mongodb
- 数据库

#### 模型预测：

- ARIMA：直接用所有数据进行预测
- bp：用训练好的模型，将使用的价格区间最后100个价格数据进入预测
- lstm：同上

- bp和lstm设置一个训练接口

#### 语言和技术：

- tensorflow
- python的flask开发后台
- 部署：使用docker-compose部署，nginx，redis，mysql，python各自的镜像结合起来

#### 接口

##### 1. 用户接口

- 1.1 注册：/user/register
- 1.2 登录：/user/login
- 1.3 修改密码：/user/alter_pwd
- 1.4 注册时发送验证码：/user/register/send_email
- 1.5 修改密码时发送验证码：/user/alter_pwd/send_email
- 1.6 查询蔬菜价格曲线：/user/vegetable/k_line
- 1.7 查询蔬菜信息：/user/vegetable/information
- 1.8 查询所有蔬菜：/user/vegetable/get_all_vegetables
- 1.9 查询今日菜价：/user/vegetable/today_price

##### 2. 模型接口

- 2.1 获取模型信息：/model/information
- 2.2 选择模型进行预测：/model/predict
- 2.3 选择网络模型进行训练，保存模型：/model/network_train
- 2.4 获取网络模型准确率：/model/get_accuracy


##### 3. 管理员接口

- 3.1 管理员增删系统的蔬菜种类：/manager/alter_vegetable
- 3.2 管理员设置用户状态（禁用功能）：/manager/set_user_state
- 3.3 管理员按照页数获取用户信息：/manager/get_user_data
- 3.4 获取用户数目：/manager/get_user_amount

##### 4. 超级管理员接口

- 4.1 超级管理员从用户中添加管理员：/root/add_manager
- 4.2 超级管理员删除管理员：/root/delete_manager

#### 完成情况

##### 2018-03-09

- 后端完成1.1 - 1.5, 3.1 - 3.2, 4.1 - 4.2接口

##### 2018-03-10

- 后端完成2.1, 2.2接口

##### 2018-03-11

- 后端以新建进程池形式完成2.3, 2.4