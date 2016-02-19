from parall_vk_api import PVkApi
import time

__author__ = 'maxim.ushakov'


class PBMemberChanges:
    def __init__(self):
        self.group_pb_folder = 'data//pb_lost_&_attended'

        self.dict_group_last = {10924683: 'main_group_last', 49067891: 'tech_group_last', 73071597: 'sport_group_last'}
        self.dict_group_change = {10924683: 'main_group_change', 49067891: 'tech_group_change', 73071597: 'sport_group_change'}

        self.date_delimiter = ':'
        self.instance_delimiter = ';'
        self.user_delimiter = ','

    def make_changes(self):
        pvk_api = PVkApi(tokens_file='data//tokens.txt')
        groups_info = pvk_api.GroupsGetMembers([i for i in self.dict_group_last.keys()])

        for group_id, group_info in groups_info.items():
            previous_members = set()
            with open(self.group_pb_folder+'//'+self.dict_group_last[group_id], 'r') as file:
                if file:
                    for row in file:
                        previous_members.add(int(row.strip('\n')))
            file.close()

            attended = []
            for member_id in group_info['users']:
                try:
                    previous_members.remove(member_id)
                except KeyError:
                    attended.append(member_id)
            lost = list(previous_members)

            with open(self.group_pb_folder+'//'+self.dict_group_last[group_id], 'w') as file:
                if group_info['users']:
                    char_str = '\n'.join([str(i) for i in group_info['users']]) + '\n'
                    file.write(char_str)
            file.close()

            with open(self.group_pb_folder+'//'+self.dict_group_change[group_id], 'a') as file:
                file.write(time.ctime(time.time())+self.date_delimiter)
                if attended:
                    char_str = self.user_delimiter.join([str(i) for i in attended])
                    file.write(char_str)
                file.write(self.instance_delimiter)
                if lost:
                    char_str = self.user_delimiter.join([str(i) for i in lost])
                    file.write(char_str)
                file.write('\n')
            file.close()






