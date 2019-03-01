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
    # 创建新用户失败，已存在用户名
    20203: {'code': 20203, 'msg': 'User already exists'},
    # 无权限
    20204: {'code': 20204, 'msg': 'None permission'},
    # 缺少蔬菜
    20301: {'code': 20301, 'msg': 'Lack vegetable'},
    # 缺少蔬菜价格
    20302: {'code': 20302, 'msg': 'Lack vegetable price'},
    # 缺少蔬菜信息
    20303: {'code': 20303, 'msg': 'Lack vegetable information'},
    # 缺少模型
    20401: {'code': 20401, 'msg': 'Lack model'},
    # 无模型信息
    20402: {'code': 20402, 'msg': 'Lack model information'}


}
