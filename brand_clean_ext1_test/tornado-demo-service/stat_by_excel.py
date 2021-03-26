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
    yundonghuwai_change = change_list_variety[0]
    xiexue_change = change_list_variety[1]
    fuzhuangkuaixiao_change = change_list_variety[2]
    row0 = ["二级分类品牌","数量","一级分类品牌","数量","差值","yundonghuwai","xiexue","fuzhuangkuaixiao"]
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
    for i in range(0, len(yundonghuwai_change)):
        sheet1.write(i + 1, 5, yundonghuwai_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(xiexue_change)):
        sheet1.write(i + 1, 6, xiexue_change[i], set_style('Times New Roman', 220, True))
    for i in range(0, len(fuzhuangkuaixiao_change)):
        sheet1.write(i + 1, 7, fuzhuangkuaixiao_change[i], set_style('Times New Roman', 220, True))
    f.save('test.xls')

def stat_difference():
    input_1 = ""
    input_2 = ""
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
    inc_data_list = ''
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


ori_data_file_1 = ""
ori_data_file_2 = ""
variety2_list = ["yundonghuwai","xiexue","fuzhuangkuaixiao"]
excel_dict = stat_difference()
variety_dict = get_variety_dict(variety2_list)
distribute_list_1 = calculate_distribute(variety_dict,variety2_list,excel_dict,ori_data_file_1)
distribute_list_2 = calculate_distribute(variety_dict,variety2_list,excel_dict,ori_data_file_2)
change_list_variety = get_change(distribute_list_1,distribute_list_2,variety2_list)
write_excel(excel_dict,change_list_variety)