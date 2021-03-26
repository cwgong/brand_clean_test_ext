# coding=utf-8
import io
import os
import bc_config
# import pymssql
import json
import re
# one_kind = []
# two_kind = []
# two2one_index = []
# two2one_dict = {}
# with io.open("./two2one_variety.txt","r",encoding="utf-8") as f:
#     lines = f.readlines()
#     for line in lines:
#         brand_item = line.split("\t")
#         one_kind.append(brand_item[1])
#         two_kind.append(brand_item[2])
#
# one_kind_set = list(set(one_kind))
# print(one_kind)
# print(one_kind_set)
# print("----------")
#
# for item in one_kind_set:
#     kind_record = []
#     for i in range(len(one_kind)):
#         if item == one_kind[i]:
#             kind_record.append(two_kind[i])
#     two2one_index.append(list(set(kind_record)))
#
# for i in range(len(one_kind_set)):
#     two2one_dict[one_kind_set[i]] = two2one_index[i]
#
# print(two2one_dict)

# legal_brand_dict = {}
# legal_brand_dict_ = {"3":[3,33,333],"4":[4,44,444]}
# legal_brand_dict__ = {"1":[1,11,111],"2":[2,22,222]}
# print(legal_brand_dict_.items())
# print(list(legal_brand_dict_.items()))
# legal_brand_dict = dict(legal_brand_dict, **legal_brand_dict_)
# print(legal_brand_dict)
# if "3" in legal_brand_dict_:
#     print(33333)
# else:
#     print(1111)
# print(legal_brand_dict_)
input_p = "C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brand_all_0701.txt"
output_p = "C:/Users/Cwgong/Desktop/temp_file/stat/dp_brands_stat_1_0701.txt"
def brand_stat_simple(input_p, output_p):
    b_dict = {}
    with open(input_p,"r",encoding="utf-8") as f2:
        for line in f2:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\x01")
            if len(lst1) != 3:
                print(lst1)
                continue
            s_id, ori_name, s_brand = lst1
            s_brand = s_brand.strip()
            if s_brand in b_dict:
                b_dict[s_brand] = b_dict[s_brand] + 1
            else:
                b_dict[s_brand] = 1
    lst2 = [(k, v) for k, v in b_dict.items()]
    lst2 = sorted(lst2, key=lambda x: x[1], reverse=True)

    lst2 = ["%s\t%s" % tmp for tmp in lst2]
    with open(output_p, 'w',encoding='utf-8') as f3:
        f3.write("\n".join(lst2))
        f3.flush()

def getting_legal_brand(cateName):
    try:
        conn = pymssql.connect(server='172.21.15.61', port='1433', \
                                    user='jiangtao', password='dpbrand123!@#', \
                                    database='o2o', charset='utf8')
        cursor = conn.cursor()
    except Exception as e:
        raise e
    try:
        legal_brand_dict = {}
        sel_sql = "select s.brand brand ,b.code code from dianping_brand_combine b join dianping_search_brand s on b.l1=s.l1  and b.l2=s.l2 where b.l1 in (select  l1 from dianping_brand_combine where code='%s')" % cateName
        cursor.execute(sel_sql)
        row = cursor.fetchall()

        for data in row:
            #self.logger.info(data[0])
            legal_brand_dict[data[0]] = data[1]
            #tmp = bytes(bytearray(data[0],  encoding='utf-8'))
            #legal_brand_dict[tmp] = data[1]
        if len(legal_brand_dict) == 0:
            err_s = "legal_brand_set is empty!"
            raise Exception(err_s)
        return legal_brand_dict
    except Exception as e:
        raise e

cate_name = ['yundonghuwai','gouwu-qita','chaoshibianli','shumachanpin','jiajujiancai','zongheshangchang','fuzhuangkuaixiao','shuiguo','huazhuangpin','xiexue']
output_file = "./out_put.json"
def add_inc_brand_data(cate_name,output_file):
    # stp2 getting legal-brand
    try:
        #传入二级分类的类目名取到二级分类下的legal_brand_dict
        cateName_list = bc_config.one2two_cateName[cate_name]
        legal_brand_dict = {}
        for cateName in cate_name:
            legal_brand_dict_ = getting_legal_brand(cateName)
            legal_brand_dict = dict(legal_brand_dict,**legal_brand_dict_)
    except Exception as e:
        raise e
    with io.open(output_file,"w",encoding="utf-8") as f:
        json.dump(legal_brand_dict,f,ensure_ascii=False)


file_list = ["C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc.2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (2).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (3).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (4).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (5).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (6).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (7).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (8).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (9).2020-07-01","C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brands_result.txt.inc (10).2020-07-01"]
def merge_variety(file_list):
    output_file = "C:/Users/Cwgong/Desktop/temp_file/stat_gouwu/dp_brand_all_0701.txt"
    for file in file_list:
        f3 = io.open(output_file, "a", encoding="utf-8")
        with open(file,encoding="utf-8") as f2:
            for line in f2:
                try:
                    f3.write(line)
                except Exception as e:
                    print(e)
        f3.close()


def get_brand_change(input_1,input_2,output_1,output_2,brand):
    brand_list1 = []
    brand_list2 = []
    f3 = io.open(output_1,"w",encoding="utf-8")     #第一个输入文件有的内容，但第二个输入文件没有
    f4 = io.open(output_2, "w", encoding="utf-8")
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

    for item in brand_list1:
        if item not in brand_list2:
            f3.write(item)
    f3.close()

    for item in brand_list2:
        if item not in brand_list1:
            f4.write(item)
    f4.close()
# brand_stat_simple(input_p,output_p)
# add_inc_brand_data(cate_name,output_file)
# merge_variety(file_list)
def generate_tab(file_p,file_out):
    data_list = []
    with io.open(file_p,"r",encoding="utf-8") as f:
        for line in f:
            line_1 = line.replace("^A","\t")
            data_list.append(line_1)

    f2 = io.open(file_out,"w",encoding="utf-8")
    for item in data_list:
        f2.write(item)
    f2.close()

def is_all_Eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def judge_brand_Eng(s_name,brand):
    if not is_all_Eng(brand):
        return brand
    s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))   #去除中文字符
    s_name_list= s_name_.split(" ")
    for item in s_name_list:
        if brand in item and len(brand) < len(item):
            return s_name
    return brand


def judge_brand_eng(self,s_name):
    ex_brand = self._real_brand_Eng_reg_(s_name)
    tmp_brand = ex_brand if ex_brand != None else s_name
    s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))  # 去除中文字符
    s_name_list = s_name_.split(" ")
    for item in s_name_list:
        item_ = item.lower()
        if tmp_brand in item_ and len(tmp_brand) < len(item_):
            return s_name
    return tmp_brand

def judge_brand_eng_(self,s_name):
    ex_brand = self._real_brand_Eng_reg_(s_name)
    tmp_brand = ex_brand if ex_brand != None else s_name    #在real_word中匹配到了就令品牌为匹配到的词，否则为店铺名
    s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))  # 去除中文字符

    s_name_merge = s_name_.replace(" ","")      #多个词组成的品牌店铺名合并
    tmp_brand_merge = tmp_brand.replace(" ","")

    ahead_rgx = re.compile("^{0}".format(tmp_brand_merge))
    behind_rgx = re.compile("{0}$".format(tmp_brand_merge))
    ahead_rgx_result = ahead_rgx.search(s_name_merge)
    behind_rgx_result = behind_rgx.search(s_name_merge)

    if ahead_rgx_result != None or behind_rgx_result != None:
        return tmp_brand
    else:
        return s_name



if __name__ == "__main__":
    # file_1 = "C:/Users/Cwgong/Desktop/totab.txt"
    # out_file = "./tab_file.txt"
    # generate_tab(file_p=file_1,file_out=out_file)
    # print(judge_brand_Eng('fantaty',"anta"))
    # print(judge_brand_Eng('lining李宁', "lining"))
    # a_name = "polo?sport"
    # t_name = "polo"
    # ahead_rgx = re.compile("^[{0}]".format(t_name))
    # behind_rgx = re.compile("[{0}]$".format(t_name))
    # print(ahead_rgx.search(a_name))
    # print(behind_rgx.search(a_name))
    # s = "?aaa."
    # print(s.strip())
    t = "asdsa"
    a = t.split("t")
    print(a)