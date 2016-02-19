# -*- coding: utf-8 -*-
from parall_vk_api import PVkApi
import api_methods as am

api = PVkApi(tokens_file='data//tokens.txt')
list_url = am.wall_get(114903384, True, 0, 4)
list_response = api.execute_all(list_url)
list_posts = am.parse_wall_get(list_response)
list_url = am.wall_addComment(114903384, True, list_posts[0].post_id, 'Third comment')
print(list_url)
#list_response = api.execute_all(list_url)
#print(list_response)

"""list_url = am.groups_getById([16757548], ['"members_count"'])
print(list_url)

list_url = ['friends.get({"user_id":64484676})',
            'friends.get({"user_id":12838221})',
            'friends.get({"user_id":239999627})',
            'friends.get({"user_id":11413041})',
            'friends.get({"user_id":98977123})',
            'friends.get({"user_id":6869656998})']
response = api.execute_all(list_url)
#print(len(response))
print(response)"""


