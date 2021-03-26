import io


class Extract_id(object):
    def __init__(self,output_file):
        self.output_file = output_file

    def write_id(self,x_list,series_data_list):
        output_list = []
        for line in series_data_list:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\x01")
            if len(lst1) != 3:
                continue
            s_id, ori_name, s_brand = lst1
            s_id = s_id.strip()
            output_list.append(s_id)
        with io.open(self.output_file,"a",encoding="utf-8") as f1:
            for sid in output_list:
                f1.write(sid + "\n")
        for item in x_list:
            print(item)