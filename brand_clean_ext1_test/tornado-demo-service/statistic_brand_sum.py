
def brand_stat_simple(input_p, output_p):
    b_dict = {}
    with open(input_p) as f2:
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
    with open(output_p, 'w') as f3:
        f3.write("\n".join(lst2))
        f3.flush()

if __name__ == "__main__":
    input_p = ""
    output_p = ""
    brand_stat_simple(input_p,output_p)