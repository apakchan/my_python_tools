import json
import pandas as pd
import os

direct_path = 'D:\\Users\\baiyuchen\\pythonProject\\my_python_tools\\data'

machine_name_list = [
    'SVR26693DE640',
    'SVR33186HW1288',
]

table_name_list = [
    'hotel',
    'hotel2',
    'resource_intl',
    'hoteloverseasextend',
    'resource_map'
]

table_dict = {
    'hotel_data_list': [],
    'hotel2_data_list': [],
    'resource_intl_data_list': [],
    'hoteloverseasextend_data_list': [],
    'resource_map_data_list': [],
}



for filename in os.listdir(direct_path):
    for table_name in table_name_list:
        file_path = os.path.join(direct_path, filename)
        if f'{table_name}.txt'.__eq__("_".join(filename.split("_")[1:])):
            with open(file_path, 'r') as f:
                for line in f:
                    json_data = json.loads(line)
                        # json_data['ip'] = []
                    # print(json_data)
                    table_dict[f'{table_name}_data_list'].append(json_data)
        # for json_data in json_data_list:
        #     print(f'{table_name}, {json_data}')
        # df = pd.json_normalize(json_data_list)
        # df.to_excel(f'{machine_name}_')
        # print(json_data_list)
        # print('===================================')

for key in table_dict.keys():
    json_list = table_dict[key]
    # print(f'============================={key}==========================================')
    # for json in json_list:
    #     print(json)
    print(f'key: {key}, size: {len(json_list)}')
    df = pd.json_normalize(json_list)
    df.to_excel(f'{key}.xlsx', index=False)
# 读取并解析txt文件
# data = []
# with open('your_file.txt', 'r') as f:
#     for line in f:
#         data.append(json.loads(line))
#
# # 将JSON数据转换为pandas的DataFrame
# df = pd.json_normalize(data)
#
# # 将DataFrame写入Excel文件
# df.to_excel('output.xlsx', index=False)
