params = {
    '/root/add_user': ['user_code', 'user_key'],
    '/root/enable_user': ['user_id'],
    '/root/disable_user': ['user_id'],
    '/customer/register_project': ['user_id', 'project_name', 'responsible_person', 'project_desc'],
    '/customer/delete_project': ['project_id'],
    '/customer/modify_project': ['project_id', 'project_name', 'responsible_person', 'project_desc'],
    '/customer/query_project': ['user_id'],
    '/customer/add_project_params': ['project_id', 'params'],
    '/customer/delete_project_params': ['project_id', 'params'],
    '/customer/query_project_params': ['project_id'],
    '/customer/add_gateway': ['project_id', 'gateway_list'],
    '/customer/delete_gateway': ['gateway_id_list'],
    '/customer/modify_gateway': ['gateway_list'],
    '/customer/query_gateway': ['project_id'],
    '/customer/query_last_data': ['gateway_id'],
    '/customer/query_history_data': ['gateway_id']
}
