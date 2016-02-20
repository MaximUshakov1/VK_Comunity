# -*- coding: utf-8 -*-
from parall_vk_api import PVkApi
import api_methods as am

api = PVkApi(tokens_file='data//tokens.txt')
list_url = am.groups_join(114903384)
list_response = api.execute_all(list_url)
list_url = am.wall_get(114903384, True, 0, 4)
list_response = api.execute_all(list_url)
list_posts = am.parse_wall_get(list_response)
print(list_posts[0].post_id)
list_url = am.wall_addComment(114903384, True, list_posts[0].post_id, 'Комментарий от Люды')
print(list_url)
list_response = api.execute_all(list_url)


