import io
import json

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
            brand_list3.append(item+'\n')

    for item in brand_list2:
        if item not in brand_list1:
            brand_list4.append(item+'\n')

    return brand_list3,brand_list4

def find_fault_data(brand_list,data_file):
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
    with io.open("./adidas_result.json","w",encoding="utf-8") as f2:
        json.dump(fault_data_list,f2,ensure_ascii=False)

def output_json(json_file):
    with io.open(json_file,"r",encoding="utf-8") as f:
        brand_list = json.load(f)
    with io.open("./adidas_result.txt","w",encoding="utf-8") as f1:
        for brand in brand_list:
            f1.write(brand)




if __name__ == "__main__":
    # data_file = ""
    # input_1 = ""
    # input_2 = ""
    # brand = "adidas"
    # brand_list_1,brand_list_2 = get_brand_change(input_1,input_2,brand)
    # find_fault_data(brand_list_1,data_file)
    json_file = "C:/Users/Cwgong/Desktop/adidas_result.json"
    output_json(json_file)