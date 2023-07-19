import requests
import json
import time
import threading


def calm_down():
    time.sleep(1)


def get_hashcode_sql(cur_machine_name, table_name, search_type):
    headers = {'Accept': 'application/json, text/plain, */*',
               'Host': 'dbtrace.ops.ctripcorp.com',
               'Content-type': 'application/json;charset=UTF-8',
               'Connection': 'keep-alive',
               'Cookie': '_RSG=L.quvbNXLsASOmjI8p1juB; _RDG=28c2d530ac8d2625b02e51e7850b50c83b; _RGUID=ad958579-79e3-4f95-be2d-073212b7061c; _bfaStatusPVSend=1; GUID=09031047410066213560; nfes_isSupportWebP=1; workbench_locale=zh-CN; PRO_CCST_SECRET_ADFC=PRO-62616979756368656e-fc99b07f823b494d9698cd394ab886c9; _ga=GA1.2.1794388953.1671691140; randomkey=eecdb7c8-28af-45a8-8ec1-c72b5287facd; usertoken=eecdb7c8-28af-45a8-8ec1-c72b5287facd; logintype=3; IFS_R=ad95857979e34f95be2d073212b7061c; FAT_cas_principal=FAT-62616979756368656e-MTY4ODM3NTcxNzEyOA-231fe76f12044ed0a7381328a6c01c41; UAT_cas_principal=UAT-62616979756368656e-MTY4ODU1OTI0NTI1MA-4a96a120afbd495db49d4eb2897b03c0; IFS_FP=pjil4d-1oe0ib3-bwrudr; _RF1=180.163.115.217; PRO_cas_principal=PRO-62616979756368656e-MTY4OTY0MzA1MDA4MQ-43ca6e903e11459f9193bf81ac83c955; PRO_principal=0e41da7ce5746321a5bb65265506385a-f378d199-1f6b-4a58-b180-5195736dc001; offlineTicket=_125F0AD8DD96586497B38479A8258DA8711506DE2DE0EFD6B9624342939F9C1A; Servers_Eid=TR020764; PRO_Servers_Eid=TR020764; _bfa=1.1659073960474.2ag57l.1.1689644006506.1689644654363.525.9.10320611903; _ubtstatus=%7B%22vid%22%3A%221659073960474.2ag57l%22%2C%22sid%22%3A525%2C%22pvid%22%3A9%2C%22pid%22%3A10320611903%7D; _bfi=p1%3D10320611903%26p2%3D10320611905%26v1%3D9%26v2%3D8; _bfaStatus=success; userInfo=%7B%22department%22%3A%22%E9%85%92%E5%BA%97%E7%A0%94%E5%8F%91%E9%83%A8%22%2C%22displayName%22%3A%22Baiyu%20Chen%20%EF%BC%88%E9%99%88%E6%9F%8F%E5%AE%87%EF%BC%89%22%2C%22employee%22%3A%22TR020764%22%2C%22mail%22%3A%22baiyuchen%40trip.com%22%2C%22name%22%3A%22baiyuchen%22%2C%22cn%22%3A%22cn1%22%7D'}

    machine_hashcode_sql_list = []

    data = {"machineName": cur_machine_name,
            "dbName": "",
            "sql": f"{search_type} {table_name} ",
            "startTime": "2023-07-18 00:00:00",
            "endTime": "2023-07-19 08:30:00",
            "pageSize": 20,
            "currentPage": 1}

    response = requests.post('http://dbtrace.ops.ctripcorp.com/api/mysql/summary', json=data, headers=headers)

    if response.status_code == 200:
        raw_hashcode_sql_json = json.loads(response.text)
        for data in raw_hashcode_sql_json['data']:
            if data.__contains__('sql') and data['sql'] is not None:
                if not data['sql'].startswith('/*'):
                    hashcode_sql = {
                        "machine_role": cur_machine_name,
                        "hashcode": data['hashcode'],
                        "sql": data['sql']
                    }
                    machine_hashcode_sql_list.append(hashcode_sql)
                else:
                    hashcode_sql = {
                        "machine_role": cur_machine_name,
                        "hashcode": data['hashcode'],
                        "sql": data['sql'],
                        "appid": data['sql'][2:11]
                    }
                    machine_hashcode_sql_list.append(hashcode_sql)
    else:
        print(f'machine_name: {cur_machine_name} error')

    return machine_hashcode_sql_list


def get_ip_set(cur_hashcode, cur_machine_id):
    if (cur_hashcode is None or len(cur_hashcode) == 0) or (cur_machine_id is None or len(cur_machine_id) == 0):
        return set()

    headers = {'Accept': 'application/json, text/plain, */*',
               'Host': 'dbtrace.ops.ctripcorp.com',
               'Content-type': 'application/json;charset=UTF-8',
               'Connection': 'keep-alive',
               'Cookie': '_RDG=28c2d530ac8d2625b02e51e7850b50c83b; _RSG=L.quvbNXLsASOmjI8p1juB; _RGUID=ad958579-79e3-4f95-be2d-073212b7061c; _bfaStatusPVSend=1; GUID=09031047410066213560; nfes_isSupportWebP=1; workbench_locale=zh-CN; PRO_CCST_SECRET_ADFC=PRO-62616979756368656e-fc99b07f823b494d9698cd394ab886c9; _ga=GA1.2.1794388953.1671691140; randomkey=eecdb7c8-28af-45a8-8ec1-c72b5287facd; usertoken=eecdb7c8-28af-45a8-8ec1-c72b5287facd; logintype=3; IFS_R=ad95857979e34f95be2d073212b7061c; FAT_cas_principal=FAT-62616979756368656e-MTY4ODM3NTcxNzEyOA-231fe76f12044ed0a7381328a6c01c41; UAT_cas_principal=UAT-62616979756368656e-MTY4ODU1OTI0NTI1MA-4a96a120afbd495db49d4eb2897b03c0; IFS_FP=pjil4d-1oe0ib3-bwrudr; _RF1=180.163.115.217; PRO_cas_principal=PRO-62616979756368656e-MTY4OTY0MzA1MDA4MQ-43ca6e903e11459f9193bf81ac83c955; PRO_principal=0e41da7ce5746321a5bb65265506385a-f378d199-1f6b-4a58-b180-5195736dc001; offlineTicket=_125F0AD8DD96586497B38479A8258DA8711506DE2DE0EFD6B9624342939F9C1A; Servers_Eid=TR020764; PRO_Servers_Eid=TR020764; _bfa=1.1659073960474.2ag57l.1.1689644006506.1689644654363.525.9.10320611903; _ubtstatus=%7B%22vid%22%3A%221659073960474.2ag57l%22%2C%22sid%22%3A525%2C%22pvid%22%3A9%2C%22pid%22%3A10320611903%7D; _bfi=p1%3D10320611903%26p2%3D10320611905%26v1%3D9%26v2%3D8; _bfaStatus=success; userInfo=%7B%22department%22%3A%22%E9%85%92%E5%BA%97%E7%A0%94%E5%8F%91%E9%83%A8%22%2C%22displayName%22%3A%22Baiyu%20Chen%20%EF%BC%88%E9%99%88%E6%9F%8F%E5%AE%87%EF%BC%89%22%2C%22employee%22%3A%22TR020764%22%2C%22mail%22%3A%22baiyuchen%40trip.com%22%2C%22name%22%3A%22baiyuchen%22%2C%22cn%22%3A%22cn1%22%7D'}

    cur_ip_set = set()

    data = {
        'db': 'mysqltracedb',
        'sql': f"select distinct client_host from v_{cur_machine_id.lower()} where hashcode= '{cur_hashcode}' and starttime >= '2023-07-19 00:00:00' and starttime <= '2023-07-19 08:30:00' order by starttime"
    }

    response = requests.post('http://dbtrace.ops.ctripcorp.com/api/sqlquery/query', json=data, headers=headers)

    if response.status_code == 200:
        json_str = json.loads(response.text)
        ip_arr = json_str['data']['rowData']
        for ip in ip_arr:
            cur_ip_set.add(ip[0])
    else:
        print(f'{cur_hashcode} {cur_machine_id} error!')

    return cur_ip_set


def get_appid(ip):
    if ip is None or len(ip) == 0:
        return None

    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Host': 'ipbook.ops.ctripcorp.com',
               'Content-type': 'application/json;charset=UTF-8',
               'Connection': 'keep-alive',
               'Cookie': '_RDG=28c2d530ac8d2625b02e51e7850b50c83b; _RSG=L.quvbNXLsASOmjI8p1juB; _RGUID=ad958579-79e3-4f95-be2d-073212b7061c; _bfaStatusPVSend=1; GUID=09031047410066213560; nfes_isSupportWebP=1; workbench_locale=zh-CN; PRO_CCST_SECRET_ADFC=PRO-62616979756368656e-fc99b07f823b494d9698cd394ab886c9; _ga=GA1.2.1794388953.1671691140; randomkey=eecdb7c8-28af-45a8-8ec1-c72b5287facd; usertoken=eecdb7c8-28af-45a8-8ec1-c72b5287facd; logintype=3; IFS_R=ad95857979e34f95be2d073212b7061c; FAT_cas_principal=FAT-62616979756368656e-MTY4ODM3NTcxNzEyOA-231fe76f12044ed0a7381328a6c01c41; UAT_cas_principal=UAT-62616979756368656e-MTY4ODU1OTI0NTI1MA-4a96a120afbd495db49d4eb2897b03c0; IFS_FP=pjil4d-1oe0ib3-bwrudr; _RF1=180.163.115.217; PRO_cas_principal=PRO-62616979756368656e-MTY4OTY0MzA1MDA4MQ-43ca6e903e11459f9193bf81ac83c955; PRO_principal=0e41da7ce5746321a5bb65265506385a-f378d199-1f6b-4a58-b180-5195736dc001; offlineTicket=_125F0AD8DD96586497B38479A8258DA8711506DE2DE0EFD6B9624342939F9C1A; Servers_Eid=TR020764; PRO_Servers_Eid=TR020764; _bfa=1.1659073960474.2ag57l.1.1689644006506.1689644654363.525.9.10320611903; _ubtstatus=%7B%22vid%22%3A%221659073960474.2ag57l%22%2C%22sid%22%3A525%2C%22pvid%22%3A9%2C%22pid%22%3A10320611903%7D; _bfi=p1%3D10320611903%26p2%3D10320611905%26v1%3D9%26v2%3D8; _bfaStatus=success'}

    data = {
        'ip': ip
    }

    response = requests.post('http://ipbook.ops.ctripcorp.com/api/serverInfo', json=data, headers=headers)

    if response.status_code == 200:
        appid_json = json.loads(response.text)
        if appid_json.__contains__('ciCode'):
            return json.loads(response.text)['ciCode']
        else:
            print(f'{ip} doesnt exists appid')
            return None
    else:
        print(f'{ip} error!')


def write_list_info_to_file(cur_list, file_name):
    if cur_list is None or len(cur_list) == 0:
        return
    if file_name is None or len(file_name) == 0:
        return

    file = open(file_name, 'w')

    for ele in cur_list:
        if ele.__contains__('appid'):
            if ele['appid'] is None or len(ele['appid']) == 0:
                ele['appid'] = list()
            else:
                ele['appid'] = list(ele['appid'])
        else:
            ele['appid'] = list()

        if ele.__contains__('ip'):
            if ele['ip'] is None or len(ele['ip']) == 0:
                ele['ip'] = list()
            else:
                ele['ip'] = list(ele['ip'])
        else:
            ele['ip'] = list()

        file.write(json.dumps(ele))
        file.write('\n')

    file.close()


def query_appid_info_write_file(cur_machine_name_list, cur_table_name):
    if cur_machine_name_list is None or cur_table_name is None or len(cur_machine_name_list) == 0 or len(cur_table_name) == 0:
        return

    for machine_name in cur_machine_name_list:
        machineId_appid_sql_info_list = []
        file_name = f'{machine_name}_{cur_table_name}.txt'
        for machine_hashcode_sql_json in get_hashcode_sql(cur_machine_name=machine_name,
                                                          table_name=cur_table_name,
                                                          search_type='from'):
            info_json = {}
            machine_id = machine_hashcode_sql_json['machine_role']
            hashcode = machine_hashcode_sql_json['hashcode']
            sql = machine_hashcode_sql_json['sql']
            if machine_hashcode_sql_json.__contains__('appid'):
                info_json = {
                    "machine_id": machine_id,
                    "hashcode": hashcode,
                    "table": cur_table_name,
                    "appid": [machine_hashcode_sql_json['appid']],
                    "sql": sql,
                }
            else:
                ip_set = get_ip_set(cur_hashcode=hashcode, cur_machine_id=machine_id)
                # when you get ip there
                # so sql is only one because hashcode is only one
                # inorder to check information
                appid_set = set()

                for ip in ip_set:
                    raw_appid_info = get_appid(ip=ip)
                    if raw_appid_info is None:
                        continue
                    appid = raw_appid_info[1:10]
                    appid_set.add(appid)
                    calm_down()

                info_json = {
                    "machine_id": machine_id,
                    "hashcode": hashcode,
                    "table": cur_table_name,
                    "appid": appid_set,
                    "ip": ip_set,
                    "sql": sql,
                }
            machineId_appid_sql_info_list.append(info_json)
            calm_down()
        write_list_info_to_file(machineId_appid_sql_info_list, file_name)
        calm_down()


if __name__ == '__main__':
    machine_name_list = [
        # 'SVR33186HW1288',  # master
        'SVR26693DE640'  # read
    ]
    search_type_list = [
        'from',
        'join'
    ]
    # HOTEL HOTEL2  RESOURCE_INTL  HOTEL_OVERSEAS_EXTEND  RESOURCE_MAP
    table_name_list = [
        'hotel',
        'hotel2',
        'resource_intl',
        'hoteloverseasextend',
        'resource_map'
    ]

    for table_name in table_name_list:
        query_appid_info_write_file(machine_name_list, table_name)
        # t = threading.Thread(target=query_appid_info_write_file, args=(machine_name_list, table_name))
        # t.start()


    # list_tmp = list({1, 2, 3})