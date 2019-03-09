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
- 1.4 查询蔬菜价格曲线：/user/vegetable/k_line
- 1.5 查询蔬菜信息：/user/vegetable/information

##### 2. 模型接口

- 2.1 获取模型信息：/model/information
- 2.2 选择模型进行预测：/model/predict
- 2.3 选择网络模型进行训练，保存模型：/model/network_train


##### 3. 管理员接口

- 3.1 管理员增删系统的蔬菜种类：/manager/alter_vegetable
- 3.2 管理员禁用用户：/manager/set_user_state

##### 4. 超级管理员接口

- 4.1 超级管理员从用户中添加管理员：/root/add_master
- 4.2 超级管理员删除管理员：/root/delete_master

