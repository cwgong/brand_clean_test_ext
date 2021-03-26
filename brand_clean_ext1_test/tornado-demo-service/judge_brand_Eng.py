import io
import os
import re

def is_all_Eng(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def is_own_Eng(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

# def _get_real_brand(base_folder):
#     # 根据real_brand进行品牌确定
#     _real_brand_p = base_folder + "/real_brand.txt"
#     if not os.path.exists(_real_brand_p):
#         raise Exception("%s does not exist!" % _real_brand_p)
#
#     real_brand_set = set()
#     with open(_real_brand_p) as f1:
#         for line in f1:
#             line = line.strip()
#             if line == "": continue
#             real_brand_set.add(line)
#
#     return real_brand_set


def _real_brand_reg_(s_name,brand_list):
    tmp_brand = None
    flag = False

    tmp_brand_list = []
    for r_b in brand_list:
        lst5 = s_name.split(r_b)
        if len(lst5) > 1:
            tmp_brand_list.append(r_b)
            flag = True

    if len(tmp_brand_list) == 0:
        return None,flag
    longest_item = tmp_brand_list[0]
    if len(tmp_brand_list) == 1:
        return longest_item,flag

    for item in tmp_brand_list:
        if len(longest_item) < len(item):
            longest_item = item
        else:
            continue

    return longest_item,flag


def judge_brand_eng(s_name,brand_list):
    ex_brand,flag = _real_brand_reg_(s_name,brand_list)
    tmp_brand = ex_brand if ex_brand != None else s_name
    s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))   #去除中文字符
    s_name_list= s_name_.split(" ")
    for item in s_name_list:
        item_ = item.lower()
        if tmp_brand in item_ and len(tmp_brand) < len(item_):
            return s_name,flag
    return tmp_brand, flag

def judge_brand_Eng(s_name,brand_list):
    ex_brand,flag = _real_brand_reg_(s_name,brand_list)
    tmp_brand = ex_brand if ex_brand != None else s_name    #在real_word中匹配到了就令品牌为匹配到的词，否则为店铺名
    s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))  # 去除中文字符

    s_name_merge = s_name_.replace(" ","")      #多个词组成的品牌店铺名合并
    tmp_brand_merge = tmp_brand.replace(" ","")

    split_result_list = s_name_merge.split(tmp_brand_merge)
    if len(split_result_list) == 1:
        return s_name,flag
    if split_result_list[0] != "" and split_result_list[1] != "":   #anta为例：tantaty情况
        return s_name,flag
    else:
        return tmp_brand,flag

    # ahead_rgx = re.compile("^{0}".format(tmp_brand_merge))
    # behind_rgx = re.compile("{0}$".format(tmp_brand_merge))
    # ahead_rgx_result = ahead_rgx.search(s_name_merge)
    # behind_rgx_result = behind_rgx.search(s_name_merge)
    #
    # if ahead_rgx_result != None or behind_rgx_result != None:
    #     return tmp_brand,flag
    # else:
    #     return s_name,flag

def s_name_dealing(ori_name):
    ori_name = ori_name.replace("|", "")
    s_name_1 = ori_name.replace('（', '(').replace("）", ")")
    lst3 = s_name_1.split('(')

    if len(lst3) >= 2:
        s_name = lst3[0]
        s_name = s_name.strip()
        if s_name == "":
            # （宇阳蔬果）瑶瑶草莓采摘
            lst4 = s_name_1.split(')')
            s_name = ori_name if len(lst4) < 2 else lst4[1]
    else:
        s_name = ori_name

    s_name = s_name.lower()
    return s_name

def get_brand_data(input_p,output_p,brand_list):
    idx = 0
    f1 = io.open(output_p, "a", encoding="utf-8")
    with open(input_p,"r",encoding="utf-8") as f:
        for line in f:
            idx += 1
            if idx % 500000 == 0: print(idx)
            line = line.strip()
            if line == "": continue

            lst1 = line.split("\t")
            if len(lst1) != 2:
                continue
            sid, ori_name = lst1
            s_name = s_name_dealing(ori_name)
            if is_own_Eng(s_name) == False:continue
            brand, flag = judge_brand_Eng(s_name,brand_list)
            if flag == True:
                brand_str = "\x01".join([sid,ori_name,brand])
                f1.write(brand_str+"\n")
    f1.close()


if __name__ == "__main__":
    # file_1 = "C:/Users/Cwgong/Desktop/totab.txt"
    # out_file = "./tab_file.txt"
    # generate_tab(file_p=file_1,file_out=out_file)
    tmp = "./eng_brand.txt"
    # brand_list = []
    # print(judge_brand_Eng('fantaty',"anta"))
    # print(judge_brand_Eng('lining李宁', "lining"))
    # with open(tmp,"r",encoding="utf-8") as f:
    #     while True:
    #         if f.readline() != "":
    #             brand_list.append(f.readline())
    #         else:
    #             break
    #
    #     for item in brand_list:
    input_p = "inc_data.txt"
    output_p = "./judge_eng.txt"
    brand_list = ["lily","cba","nba","only","vero moda","five plus"]
    get_brand_data(input_p,output_p,brand_list)