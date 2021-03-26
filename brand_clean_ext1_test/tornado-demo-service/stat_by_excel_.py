import xlwt
import io


def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def write_excel(excel_dict,change_list_variety):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('brand_stat',cell_overwrite_ok=True)
    variety1_list = excel_dict['variety1_list']
    variety1_num_list = excel_dict['variety1_num_list']
    variety3_list = excel_dict['variety3_list']
    variety3_num_list = excel_dict['variety3_num_list']
    difference_value_list = excel_dict['difference_value_list']
    huoguo_change = change_list_variety[0]
    yinpindian_change = change_list_variety[1]
    kafeiting_change = change_list_variety[2]
    xican_change = change_list_variety[3]
    shaokao_change = change_list_variety[4]
    mianbaotiandian_change = change_list_variety[5]
    xiaochikuaican_change = change_list_variety[6]
    meishi_change = change_list_variety[7]
    luwei_change = change_list_variety[8]
    row0 = ["二级分类品牌","数量","一级分类品牌","数量","差值","huoguo","yinpindian","kafeiting","xican","shaokao","mianbaotiandian","xiaochikuaican","meishi-qita","luwei"]
    colum0 = ["张三","李四","恋习Python","小明","小红","无名"]
    #写第一行
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
    #写第一列
    for i in range(0,len(variety1_list)):
        sheet1.write(i+1,0,variety1_list[i],set_style('Times New Roman',220,True))
    for i in range(0,len(variety1_num_list)):
        sheet1.write(i+1,1,variety1_num_list[i],set_style('Times New Roman',220,True))
    for i in range(0,len(variety3_list)):
        sheet1.write(i+1,2,variety3_list[i],set_style('Times New Roman',220,True))
    for i in range(0,len(variety3_num_list)):
        sheet1.write(i+1,3,variety3_num_list[i],set_style('Times New Roman',220,True))
    for i in range(0,len(difference_value_list)):
        sheet1.write(i+1,4,difference_value_list[i],set_style('Times New Roman',220,True))
    for i in range(0, len(huoguo_change)):
        sheet1.write(i + 1, 5, huoguo_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(yinpindian_change)):
        sheet1.write(i + 1, 6, yinpindian_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(kafeiting_change)):
        sheet1.write(i + 1, 7, kafeiting_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(xican_change)):
        sheet1.write(i + 1, 8, xican_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(shaokao_change)):
        sheet1.write(i + 1, 9, shaokao_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(mianbaotiandian_change)):
        sheet1.write(i + 1, 10, mianbaotiandian_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(xiaochikuaican_change)):
        sheet1.write(i + 1, 11, xiaochikuaican_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(meishi_change)):
        sheet1.write(i + 1, 12, meishi_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(luwei_change)):
        sheet1.write(i + 1, 13, luwei_change[i], set_style('Times New Roman', 220, True))
    f.save('brand_result_.xls')

def stat_difference():
    input_1 = "./stat_brand_10_result.txt"
    input_2 = "./stat_brand_1_result.txt"
    top_num = 100
    variety1_list = []
    variety1_num_list = []
    variety2_list = []
    variety2_num_list = []
    variety3_list = []
    variety3_num_list = []
    difference_value_list = []
    with io.open(input_1,"r",encoding="utf-8") as f1:
        for line in f1:
            top_num = top_num - 1
            line = line.strip()
            if line == "": continue
            line_list = line.split("\t")
            if len(line_list) != 2:
                print(line_list)
                continue
            brand1,brand1_num = line_list
            variety1_list.append(brand1)
            variety1_num_list.append(brand1_num)
            if top_num <= 0:
                break

    with io.open(input_2,"r",encoding="utf-8") as f2:
        for line in f2:
            line = line.strip()
            if line == "": continue
            line_list = line.split("\t")
            if len(line_list) != 2:
                print(line_list)
                continue
            brand2,brand2_num = line_list
            variety2_list.append(brand2)
            variety2_num_list.append(brand2_num)

    for item1 in variety1_list:
        for i in range(len(variety2_list)):
            if item1 == variety2_list[i]:
                variety3_list.append(variety2_list[i])
                variety3_num_list.append(variety2_num_list[i])
                break
            else:
                continue

    for j in range(len(variety1_num_list)):
        difference_value_list.append(int(variety3_num_list[j]) - int(variety1_num_list[j]))

    excel_dict = {
        "variety1_list":variety1_list,
        "variety1_num_list": variety1_num_list,
        "variety3_list": variety3_list,
        "variety3_num_list": variety3_num_list,
        "difference_value_list":difference_value_list
    }

    return excel_dict

def get_variety_dict(variety2_list):
    variety_dict = {}
    flag = 0
    inc_data_list = ['/home/supdev/gongchengwei/brand_clean_ext_test/0-1-huoguo/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/0-3-yinpindian/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/0-4-kafeiting/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/4-xican/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/2-shaokao/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/3-mianbaotiandian/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/9-00-xiaochikuaican/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/9-10-qita/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01','/home/supdev/gongchengwei/brand_clean_ext_test/5-luwei/inc_v1/inc_data/dp_brands_result.txt.inc.2020-07-01']
    for inc_data in inc_data_list:
        variety = variety2_list[flag]
        flag = flag + 1
        with io.open(inc_data,"r",encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                line_list = line.split("\x01")
                if len(line_list) != 3:
                    continue
                sid, ori_name, s_name = line_list
                variety_dict[sid] = variety

    return variety_dict

def calculate_distribute(variety_dict,variety2_dict,excel_dict,ori_data_file):
    distribute_list = []
    brand_list = excel_dict["variety1_list"]
    for brand in brand_list:
        temp_dict = {}
        for variety2 in variety2_dict:
            temp_dict[variety2] = 0
        f1 = io.open(ori_data_file, "r", encoding="utf-8")
        for line in f1:
            line = line.strip()
            if line == "": continue
            line_list = line.split("\x01")
            if len(line_list) != 3:
                continue
            sid, ori_name, s_name = line_list
            if s_name != brand:continue
            if sid not in variety_dict:continue
            variety_temp = variety_dict[sid]
            temp_dict[variety_temp] = temp_dict[variety_temp] + 1
        f1.close()
        distribute_list.append(temp_dict)
    return distribute_list

def get_change(variety_dict_1,variety_dict_2,variety2_list):
    change_list = []
    change_list_variety = []
    for i in range(len(variety_dict_2)):
        temp_dict = {}
        for item in variety2_list:
            temp_dict[item] = variety_dict_1[i][item] - variety_dict_2[i][item]
        change_list.append(temp_dict)

    for item in variety2_list:
        item_list = []
        for change_dict in change_list:
            item_list.append(change_dict[item])
        change_list_variety.append(item_list)
    return change_list_variety

def get_brand_single_change():
    brand_list1 = []
    brand_list2 = []
    brand_list3 = []
    brand_list4 = []
    # f3 = io.open(output_1,"w",encoding="utf-8")     #第一个输入文件有的内容，但第二个输入文件没有
    # f4 = io.open(output_2, "w", encoding="utf-8")
    with io.open(input_1, "r", encoding="utf-8") as f1:
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
            brand_list3.append(item + '\n')

    for item in brand_list2:
        if item not in brand_list1:
            brand_list4.append(item + '\n')
    print(len(brand_list4))
    return brand_list3, brand_list4


ori_data_file_1 = "./brand_result_1_all_duplicate.txt"
ori_data_file_2 = "./brand_result_10_all_duplicate.txt"
variety2_list = ["huoguo","yinpindian","kafeiting","xican","shaokao","mianbaotiandian","xiaochikuaican","meishi-qita","luwei"]
excel_dict = stat_difference()
variety_dict = get_variety_dict(variety2_list)
distribute_list_1 = calculate_distribute(variety_dict,variety2_list,excel_dict,ori_data_file_1)
distribute_list_2 = calculate_distribute(variety_dict,variety2_list,excel_dict,ori_data_file_2)
change_list_variety = get_change(distribute_list_1,distribute_list_2,variety2_list)
write_excel(excel_dict,change_list_variety)
