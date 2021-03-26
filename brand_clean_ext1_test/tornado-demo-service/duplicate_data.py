import io

def duplicate_data(input_1,output_1):
    id_dict = {}
    duplicate_list = []
    length = 0
    with io.open(input_1,"r",encoding="utf-8") as f:
        for line in f:
            length = length + 1
            line = line.strip()
            if line == "":continue
            line_list = line.split("\x01")
            if len(line_list) != 3:
                continue
            sid,ori_name,s_name = line_list
            if sid in id_dict:
                continue
            else:
                id_dict[sid] = ""
                duplicate_list.append(line+"\n")
    print(length)
    print(len(duplicate_list))
    with io.open(output_1,"w",encoding="utf-8") as f1:
        for item in duplicate_list:
            f1.write(item)

if __name__ == "__main__":
    input_1 = ''
    output_1 = ''
    duplicate_data(input_1,output_1)
