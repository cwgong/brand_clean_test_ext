#!/usr/bin/env python
#coding=utf-8

import sys
import os

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

def line_deal(line, bug_s, right_brand):
    line = line.strip()
    lst1 = line.split('\x01')
    if len(lst1) != 3:
        print(line)
        return None

    sid, ori_name, sbrand = lst1
    s_name = s_name_dealing(ori_name)
    sbrand = sbrand.strip()

    if sbrand == bug_s:
        return s_name + "|" + right_brand
    else:
        return None

def brand_stat_simple(input_p, output_p):
    if not os.path.exists(input_p):
        print("%s does not exist!" % input_p)
        sys.exit(-1)
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

