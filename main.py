# -*- coding: utf-8 -*-

from parall_vk_api import PVkApi
import api_methods as am

api = PVkApi(tokens_file='data//tokens.txt')
"""
file_in = open('data//участники_по участию в группе', 'r')
user_list = []
for row in file_in:
    user_list.append(int(row.strip('\n')))
file_in.close()

url_list = []
for user in user_list:
    url_list.extend(am.groups_get(user, 1))

response_list = api.execute_all(url_list)"""


"""url_list = []
for user in user_list[0:2]:
    url_list.extend(am.users_get([user], ['counters']))

response_list = api.execute_all(url_list)
user_list = am.parse_users_get(response_list, ['counters'])

for user in user_list:
    print(user['id'], user['counters'])"""

"""file_out = open('data//users-groups', 'w')
for index in range(len(user_list)):
    try:
        file_out.writelines('%d,%d\n' % (user_list[index], response_list[index][0]))
    except:
        file_out.writelines('%d,%d\n' % (user_list[index], 0))
file_out.close()"""

"""file_in = open('data//friends', 'r')
file_out = open('data//friends_count', 'w')

for row in file_in:
    new_row = row.split(':')[0]
    file_out.writelines(new_row+'\n')

file_in.close()
file_out.close()"""

url_list = am.wall_get(10924683, True, 1, 1)
response_list = api.execute_all(url_list)
post_list = am.parse_wall_get(response_list)

post = post_list[0]

print(post.owner_id)

url_list = am.wall_getReposts(10924683, True, post.post_id)
response_list = api.execute_all(url_list)
reposters_list = am.parse_wall_getReposts(response_list)
print(reposters_list)