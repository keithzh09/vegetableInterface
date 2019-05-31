params = {
    '/user/register': ['user_name', 'password', 'check_password', 'email', 'email_code'],
    '/user/login': ['user_name', 'password'],
    '/user/alter_pwd': ['user_name', 'new_password', 're_password', 'email', 'email_code'],
    '/user/vegetable/k_line': ['vegetable_name', 'date'],
    '/user/vegetable/information': ['vegetable_name'],
    '/model/information': ['model_name'],
    '/model/predict': ['model_name', 'vegetable_name', 'start_date'],
    '/model/network_train': ['model_name', 'vegetable_name'],
    '/model/get_accuracy': ['model_name', 'vegetable_name'],
    '/manager/alter_vegetable': ['vegetable_name', 'vegetable_information', 'operate_type'],
    '/manager/set_user_state': ['user_name', 'user_state'],
    '/root/add_master': ['user_name'],
    '/root/delete_master': ['user_name']

}
