response = {
    # 操作成功
    200: {'code': 200, 'msg': 'Handle Successfully'},
    # 操作失败,未知错误
    -200: {'code': -200, 'msg': 'Handle Failed'},
    # 缺少参数
    # 缺少body参数
    20101: {'code': 20101, 'msg': 'Lack body param'},
    # 缺少header参数
    20102: {'code': 20102, 'msg': 'Lack header param'},
    # 参数无效,token过期
    20103: {'code': 20103, 'msg': 'Invalid header param'},
    # 登录接口，校验失败: 无此用户或密码错误
    # 用户不存在
    20201: {'code': 20201, 'msg': 'User does not exist'},
    # 密码错误
    20202: {'code': 20202, 'msg': 'Password error'},
    # 无权限
    20203: {'code': 20203, 'msg': 'None permission'},
    # 注册接口
    # 创建新用户失败，已存在用户名
    20301: {'code': 20301, 'msg': 'User already exists'},
    # 用户名格式错误
    20302: {'code': 20302, 'msg': 'User name format error'},
    # 密码格式错误
    20303: {'code': 20303, 'msg': 'User name format error'},
    # 两次密码输入不一样
    20304: {'code': 20304, 'msg': 'Two password entries are different'},
    # 邮箱验证码错误
    20305: {'code': 20305, 'msg': 'Email_code is wrong'},
    # 邮箱已被使用
    20306: {'code': 20306, 'msg': 'Email is used'},
    # 邮箱格式错误
    20307: {'code': 20307, 'msg': 'Email format error'},
    # 用户名和邮箱不匹配
    20308: {'code': 20308, 'msg': 'User and email do not match'},
    # 缺少蔬菜
    20401: {'code': 20401, 'msg': 'Lack vegetable'},
    # 缺少蔬菜价格
    20402: {'code': 20402, 'msg': 'Lack vegetable price'},
    # 缺少蔬菜信息
    20403: {'code': 20403, 'msg': 'Lack vegetable information'},
    # 缺少模型id
    20501: {'code': 20501, 'msg': 'Lack model id'},
    # 无模型信息
    20502: {'code': 20502, 'msg': 'Lack model information'}
}
