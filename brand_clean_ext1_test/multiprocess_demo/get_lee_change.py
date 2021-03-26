import io
import json
import math
import multiprocessing
import time

def deal_data(data_list,epoch):
    tmp_list = []
    series_data_list = []
    for i in range(epoch):
        tmp_list = data_list[math.floor(i*len(data_list)/epoch):math.floor((i+1)*len(data_list)/epoch)]
        series_data_list.append(tmp_list)

    for series_data in series_data_list:
        print(len(series_data))
    return series_data_list


def get_brand_change(input_1,input_2,brand):
    brand_list1 = []
    brand_list2 = []
    brand_list3 = []
    brand_list4 = []
    # f3 = io.open(output_1,"w",encoding="utf-8")     #第一个输入文件有的内容，但第二个输入文件没有
    # f4 = io.open(output_2, "w", encoding="utf-8")
    with io.open(input_1,"r",encoding="utf-8") as f1:
        for line in f1:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\x01")
            if len(lst1) != 3:
                print(lst1)
                continue
            s_id, ori_name, s_brand = lst1
            s_brand = s_brand.strip()
            if s_brand == brand:
                brand_list1.append(line)
    print(len(brand_list1))
    with io.open(input_2, "r", encoding="utf-8") as f2:
        for line in f2:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\x01")
            if len(lst1) != 3:
                print(lst1)
                continue
            s_id, ori_name, s_brand = lst1
            s_brand = s_brand.strip()
            if s_brand == brand:
                brand_list2.append(line)
    print(len(brand_list2))
    for item in brand_list1:
        if item not in brand_list2:
            brand_list3.append(item+'\n')

    for item in brand_list2:
        if item not in brand_list1:
            brand_list4.append(item+'\n')
    print(len(brand_list4))
    return brand_list3,brand_list4

def find_fault_data(brand_list):
    print(len(brand_list))
    data_file = "./brand_result_2_all_duplicate.txt"
    output_1 = "./lee2_result_thread.txt"
    def split_id(line):
        line = line.strip()
        if line == "": return ""
        line_list = line.split("\x01")
        if len(line_list) != 3:
            return ""
        sid, ori_name, s_name = line_list
        return sid
    ori_data_list = []
    fault_data_list = []
    with io.open(data_file,"r",encoding="utf-8") as f1:
        for line in f1:
            ori_data_list.append(line)
    for brand in brand_list:
        brand_id = split_id(brand)
        if brand_id == "":continue
        for line in ori_data_list:
            line_id = split_id(line)
            if line_id == brand_id:
                fault_data_list.append(line)
                break
            else:
                continue
    with io.open(output_1,"w",encoding="utf-8") as f2:
        for line in fault_data_list:
            f2.write(line)

def find_fault_data_2(brand_list):
    print(len(brand_list))
    data_file = "./brand_result_1_all_duplicate.txt"
    output_1 = "./lee1_result_thread.txt"
    def split_id(line):
        line = line.strip()
        if line == "": return ""
        line_list = line.split("\x01")
        if len(line_list) != 3:
            return ""
        sid, ori_name, s_name = line_list
        return sid
    ori_data_list = []
    fault_data_list = []
    with io.open(data_file,"r",encoding="utf-8") as f1:
        for line in f1:
            ori_data_list.append(line)
    for brand in brand_list:
        brand_id = split_id(brand)
        if brand_id == "":continue
        for line in ori_data_list:
            line_id = split_id(line)
            if line_id == brand_id:
                fault_data_list.append(line)
                break
            else:
                continue
    with io.open(output_1,"w",encoding="utf-8") as f2:
        for line in fault_data_list:
            f2.write(line)


if __name__ == "__main__":
    data_file = "./brand_result_2_all_duplicate.txt"
    data_file1 = "./brand_result_1_all_duplicate.txt"
    input_1 = "brand_result_1_all_duplicate.txt"
    input_2 = "brand_result_2_all_duplicate.txt"
    brand = "lee"
    output_1 = "./lee2_result_thread.txt"
    output_2 = "./lee1_result_thread.txt"
    epoch = 10
    time1 = time.time()
    brand_list_1,brand_list_2 = get_brand_change(input_1,input_2,brand)
    pool = multiprocessing.Pool(epoch)
    series_data_list1 = deal_data(brand_list_1,epoch=epoch)
    series_data_list2 = deal_data(brand_list_2, epoch=epoch)
    pool.map(find_fault_data,series_data_list1)
    pool.map(find_fault_data_2, series_data_list2)
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')
