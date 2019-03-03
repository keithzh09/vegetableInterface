params = {
    '/user/register': ['user_name', 'password', 'email', 'email_code'],
    '/user/login': ['user_name', 'password'],
    '/user/alter_pwd': ['user_name', 'new_password', 're_password', 'email', 'email_code'],
    '/user/model/information': [],
    '/user/model/predict': ['model_name', 'vegetable_name', 'date', 'days'],
    '/vegetable/k_line': ['vegetable_name', 'date'],
    '/vegetable/information': ['vegetable_name'],
    '/master/alter_vegetable': ['vegetable_name', 'operate_type']

}
