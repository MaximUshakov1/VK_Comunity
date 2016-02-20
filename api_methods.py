import json
import urllib.parse as url_p


class Post:
    def __init__(self, post_id, owner_id, date, num_comments=-1, num_likes=-1, num_reposts=-1):
        self.post_id = post_id
        self.owner_id = owner_id
        self.date = date
        self.num_comments = num_comments
        self.num_likes = num_likes
        self.num_reposts = num_reposts


def groups_getById(group_ids, fields):
    class_name = 'groups'
    method_name = 'getById'
    max_group_ids = 500

    url_list = []

    group_ids_temp = group_ids.copy()
    while len(group_ids_temp) > max_group_ids:
        sub_group_ids = group_ids_temp[0:max_group_ids]
        group_ids_temp = group_ids_temp[max_group_ids:]
        options = ('"group_ids":'+','.join([str(group_id) for group_id in sub_group_ids]) +
                   ',"fields":'+','.join(fields))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)
    if len(group_ids_temp) > 0:
        options = ('"group_ids":'+','.join([str(group_id) for group_id in group_ids_temp]) +
                   ',"fields":'+','.join(fields))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)

    return url_list


def groups_getMembers(group_id, count, offset=0):
    class_name = 'groups'
    method_name = 'getMembers'
    max_count_members = 1000

    url_list = []

    count_members_temp = count
    offset_temp = offset
    while count_members_temp > max_count_members:
        options = ('"group_id":'+str(group_id) +
                   ',"offset":'+str(offset_temp) +
                   ',"count":'+str(max_count_members))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)

        offset_temp += max_count_members
        count_members_temp -= max_count_members
    if count_members_temp > 0:
        options = ('"group_id":'+str(group_id) +
                   ',"offset":'+str(offset_temp) +
                   ',"count":'+str(count_members_temp))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)

    return url_list


def groups_join(group_id):
    class_name = 'groups'
    method_name = 'join'

    url_list = []

    options = '"group_id":'+str(group_id)
    url = '%s.%s({%s})' % (class_name, method_name, options)
    url_list.append(url)

    return url_list


def parse_groups_join(response_list):
    list_success = []
    for response in response_list:
        if response == '1':
            list_success.append(1)
        else:
            list_success.append(0)
    return list_success


def wall_get(owner_id, is_group, offset, count):
    if is_group:
        owner_id = - owner_id

    class_name = 'wall'
    method_name = 'get'
    max_count_posts = 100

    url_list = []

    count_posts_temp = count
    offset_temp = offset
    while count_posts_temp > max_count_posts:
        options = ('"owner_id":'+str(owner_id) +
                   ',"offset":'+str(offset_temp) +
                   ',"count":'+str(max_count_posts) +
                   ',"filter":'+'"owner"' +
                   ',"extended":'+str(0))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)

        offset_temp += max_count_posts
        count_posts_temp -= max_count_posts
    if count_posts_temp > 0:
        options = ('"owner_id":'+str(owner_id) +
                   ',"offset":'+str(offset_temp) +
                   ',"count":'+str(count_posts_temp) +
                   ',"filter":'+'"owner"' +
                   ',"extended":'+str(0))
        url = '%s.%s({%s})' % (class_name, method_name, options)
        url_list.append(url)

    return url_list


def parse_wall_get(response_list):
    list_post = []
    for response in response_list:
        list_posts_response = response
        """try:
            list_posts_response = response.get('items')
        except:
            print('Bad response (wall.get): ', response)
            continue"""

        for post_response in list_posts_response[1:]:
            try:
                post_id = int(post_response.get('id'))
            except:
                print('Bad response id (wall.get): ', post_response)
                continue

            try:
                owner_id = int(post_response.get('to_id'))
            except:
                print('Bad response owner_id (wall.get): ', post_response)
                continue

            try:
                date = int(post_response.get('date'))
            except:
                print('Bad response date (wall.get): ', post_response)
                continue

            try:
                num_comments = int(post_response.get('comments').get('count'))
            except:
                num_comments = 0

            try:
                num_likes = int(post_response.get('likes').get('count'))
            except:
                num_likes = 0

            try:
                num_reposts = int(post_response.get('reposts').get('count'))
            except:
                num_reposts = 0

            list_post.append(Post(post_id, owner_id, date, num_comments, num_likes, num_reposts))
    return list_post


def wall_addComment(owner_id, is_group, post_id, text):
    if is_group:
        owner_id = - owner_id

    class_name = 'wall'
    method_name = 'addComment'

    url_list = []

    #print(urlencode(text))

    temp_row = url_p.urlencode({'1':text}, quote_via=url_p.quote)
    text = temp_row.split('=')[1]
    #options = url_p.urlencode({'"owner_id"': owner_id, '"post_id"': post_id, '"text"': text}, quote_via=url_p.quote)
    #print(options)
    options = ('"owner_id":'+str(owner_id) +
               ',"post_id":'+str(post_id) +
               ',"text":'+'"%s"' % text)
    url = '%s.%s({%s})' % (class_name, method_name, options)
    url_list.append(url)

    return url_list


