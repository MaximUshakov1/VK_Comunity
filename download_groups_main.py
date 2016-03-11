# -*- coding: utf-8 -*-
from parall_vk_api import PVkApi
import api_methods as am

# инициализация модуля api
api = PVkApi(tokens_file='data//tokens.txt')

# считывание участников, на которых ориентируемся
user_list = []

file_in = open('file_name', 'r')
for row in file_in:
    user_list.append(int(row.strip('\n')))
file_in.close()

# !!! 1 стадия выгрузки !!!
# выгружаем группы, на которые подписаны юзеры
group_set = set()  # множество всех выгруженных групп
# делим юзеров на пачки чтобы сохранять промежуточные результаты
pack_size = 10000
urls_per_user = 5  # количество url, нужных для выгрузки групп одного участника
check_group1 = 10924683  # группы, по которым можно чекать, запривачена ли страничка, или нет
check_group2 = 49067891
file_out = open('data_out', 'a')  # файл для промежуточного вывода, должен быть заранее создан
obtained_user_count = 0  # по скольки юзерам информация уже получена
for i in range(len(user_list) // pack_size):
    # составляем пачку юзеров
    pack_user_list = user_list[obtained_user_count : (obtained_user_count+pack_size)]
    obtained_user_count += pack_size

    # готовим список url-ов для выгрузки
    url_list = []
    for user in pack_user_list:
        url_list.extend(am.groups_get(user, count=5000, offset=0))

    # закидываем всё в execute и записываем результат
    response_list = api.execute_all(url_list)
    groups_list = am.parse_groups_get(response_list)

    # записываем результат в файл
    for j in range(pack_size):
        user_group_dict = {}
        user_group_dict['id'] = pack_user_list[j]
        user_group_dict['groups'] = []
        for k in range(urls_per_user):
            user_group_dict['groups'].extend(groups_list[j*pack_size+k])
        user_group_dict['count'] = len(user_group_dict['groups'])
        user_group_dict['is_private'] = 0 if check_group1 in set(user_group_dict['groups']) or\
                                             check_group2 in set(user_group_dict['groups']) else 1
        file_out.writelines('%d;%d;%d:%s\n' % (user_group_dict['id'], user_group_dict['count'], user_group_dict['is_private'],
                                               ','.join([str(group_id) for group_id in user_group_dict['groups']])))

# то же самое для последней пачки, если она есть
if obtained_user_count < len(user_list):
    # составляем пачку юзеров
    pack_user_list = user_list[obtained_user_count : ]

    # готовим список url-ов для выгрузки
    url_list = []
    for user in pack_user_list:
        url_list.extend(am.groups_get(user, count=5000, offset=0))

    # закидываем всё в execute и записываем результат
    response_list = api.execute_all(url_list)
    groups_list = am.parse_groups_get(response_list)

    # записываем результат в файл
    for j in range(len(pack_user_list)):
        user_group_dict = {}
        user_group_dict['id'] = pack_user_list[j]
        user_group_dict['groups'] = []
        for k in range(urls_per_user):
            user_group_dict['groups'].extend(groups_list[j*pack_size+k])
        user_group_dict['count'] = len(user_group_dict['groups'])
        user_group_dict['is_private'] = 0 if check_group1 in set(user_group_dict['groups']) or\
                                             check_group2 in set(user_group_dict['groups']) else 1
        file_out.writelines('%d;%d;%d:%s\n' % (user_group_dict['id'], user_group_dict['count'], user_group_dict['is_private'],
                                               ','.join([str(group_id) for group_id in user_group_dict['groups']])))

        group_set |= set(user_group_dict['groups'])

file_out.close()

# выгружаем список всех групп
file_out = open('all_groups', 'w')
for group in group_set:
    file_out.writelines('%d\n' % group)
file_out.close()
# !!! конец 1 стадии выгрузки !!!

# !!! 2 стадия выгрузки !!!
# считываем все выгруженные группы
group_list = []

file_in = open('all_groups', 'r')
for row in file_in:
    group_list.append(int(row.strip('\n')))
file_in.close()

# для считанных групп определяем их тип
url_list = am.groups_getById(group_list, [])
response_list = api.execute_all(url_list)
group_info_list = am.parse_groups_getById(response_list, [])

# записываем информацию о группах в файл
file_out = open('all_groups_info', 'w')
for group_obj in group_info_list:
    file_out.writelines('%s;%s;%s;%s\n' % (group_obj['id'], group_obj['name'],
                                           group_obj['screen_name'], group_obj['type']))
file_out.close()
# для всех юзеров с заприваченными страницами проверяем их принадлежность к выгруженным группам
# делим юзеров на пачки чтобы сохранять промежуточные результаты