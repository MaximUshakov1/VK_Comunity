# -*- coding: utf-8 -*-
from threading import Thread
from urllib.request import urlopen
import json
import time


class PVkApi:
    def __init__(self, tokens=[], tokens_file = ''):
        self.tokens = []

        self.ExecuteInsideMethodsCount = 25 #количество методов, которое будет использованно при вызове метода Execute
        self.MethodsUrl = 'https://api.vk.com/method/' #url для вызова методов
        self.ExceptSleepTime = 2 #время, которое будет ожидать метод при получении ошибки
        self.QuerysSleepTime = 0.25 #минимальное время, между запросами
        self.ExceptCountMax = 10 #Максимальное количество подряд идущих исключний

        if len(tokens):
            self.set_tokens(tokens)
        elif len(tokens_file):
            self.read_tokens(tokens_file)

    def read_tokens(self, tokens_file):
        with open(tokens_file, 'r') as File:
            rows = File.read().split('\n')
            for row in rows:
                if rows:
                    self.tokens.append(row)

    def set_tokens(self, tokens):
        self.tokens = [token for token in tokens]

    def execute(self, url_list, token, response_list=[]):
        url_request = self.MethodsUrl+'execute?code=return{'
        execute_key = 0
        previous_time = 0
        for url in url_list:
            url_request += '"execute_%d":API.%s,' % (execute_key, url)
            execute_key += 1
            if execute_key == self.ExecuteInsideMethodsCount:
                url_request = url_request.strip(',')
                url_request += '};&access_token=%s' % token
                current_time = time.clock()
                if (current_time - previous_time) < self.QuerysSleepTime:
                    time.sleep(current_time - previous_time)

                #print(len(url_request), url_request)
                except_count = 0
                while except_count <= self.ExceptCountMax:
                    url_object = urlopen(url_request)
                    previous_time = time.clock()
                    text_response = str(url_object.read().decode())
                    response = json.loads(text_response).get('response')
                    if not response:
                        except_count += 1
                        time.sleep(self.ExceptSleepTime)
                    else:
                        break

                if response:
                    for method_id in range(execute_key):
                        response_list.append(response.get('execute_'+str(method_id)))
                else:
                    print('Error:' + url_request)
                    for method_id in range(execute_key):
                        response_list.append([])
                url_request = self.MethodsUrl+'execute?code=return{'
                execute_key = 0

        if execute_key > 0:
            url_request = url_request.strip(',')
            url_request += '};&access_token=%s' % token

            print(len(url_request), url_request)
            except_count = 0
            while except_count <= self.ExceptCountMax:
                url_object = urlopen(url_request)
                text_response = str(url_object.read().decode())
                response = json.loads(text_response).get('response')
                if not response:
                    except_count += 1
                    time.sleep(self.ExceptSleepTime)
                else:
                    break

            if response:
                for method_id in range(execute_key):
                    response_list.append(response.get('execute_'+str(method_id)))
            else:
                print('Error:' + url_request)
                for method_id in range(execute_key):
                    response_list.append([])

        return response_list

    def execute_all(self, url_list):
        num_methods_for_every_job = len(url_list) // len(self.tokens)
        num_methods_for_every_job += 1

        response_list = []
        response_dict_lists = {}

        jobs = {}
        for i in range(len(self.tokens)):
            small_url_list = url_list[(i*num_methods_for_every_job):min((i+1)*num_methods_for_every_job, len(url_list))]
            response_dict_lists[i] = []
            jobs[i] = Thread(target=self.execute, args=(small_url_list.copy(), self.tokens[i], response_dict_lists[i]))
            jobs[i].start()
        for i in range(len(self.tokens)):
            jobs[i].join()
            response_list.extend(response_dict_lists[i])

        return response_list