#!/usr/bin/env python3
#coding=utf-8

"""
todo: 李威清洗的数据[火锅、化妆品、饮品店、咖啡厅]，在我的方法里执行有问题
原因：处理逻辑不同造成的
解决方法：1）获取合法的品牌 2）找到增量的数据 3）增量数据字符串中出现了合法品牌，就将这个品牌赋予它
"""

import sys
import os
import time
import shutil
import traceback
from mssql_opt import MsSqlOpt
import tool

class LiweiBrandClean(object):
    def __init__(self, legal_brand_dict, base_folder, log_instance, bc_date):
        brandreg_p = base_folder + "/dp_brands_result.txt.brandreg"
        if not os.path.exists(brandreg_p):
            raise Exception("%s does not exists!" % brandreg_p)
        inc_data_p = base_folder + "/inc_data/inc_data.txt"
        if not os.path.exists(inc_data_p):
            raise Exception("%s does not exists!" % inc_data_p)

        inc_result_p = base_folder + "/inc_data/dp_brands_result.txt.inc." + bc_date
        inc_stat_p = base_folder + "/inc_data/dp_statistics.txt.inc." + bc_date

        self.logger = log_instance
        self._ori_p = brandreg_p
        self._inc_p = inc_data_p
        self._output_p = inc_result_p
        self._inc_data_stat = inc_stat_p
        self._legal_brand_dict = legal_brand_dict
        self._old_sid_dict, self._old_data = self._get_ori_brand_dict()
        if len(self._old_data) < 1:
            raise Exception("%s data is empty!!" % brandreg_p)

    def _get_ori_brand_dict(self):
        if not os.path.exists(self._ori_p):
            raise Exception("%s does not exist!" % self._ori_p)

        sid_dict = {}
        old_lst = []
        with open(self._ori_p) as f2:
            for line in f2:
                line = line.strip()
                if line == "": continue
                old_lst.append(line)
                lst1 = line.split("\x01")
                if len(lst1) != 3:
                    self.logger.info("ori_brand error data: %s" % line)
                    continue
                s_id, ori_name, s_brand = lst1
                s_id = s_id.strip()
                sid_dict[s_id.strip()] = 0
        self.logger.info("len of old_data: %s" % len(old_lst))
        return sid_dict, old_lst

    def _brand_reg(self,s_name):
        tmp_brand_lst = []
        for k, v in self._legal_brand_dict.items():
            lst1 = s_name.split(k)
            if len(lst1) >= 2:
                # has problem
                tmp_brand_lst.append((k, len(k)))
        if len(tmp_brand_lst) == 0:
            return s_name
        else:
            tmp_brand_lst = sorted(tmp_brand_lst, key=lambda x: x[1], reverse=True)
            return tmp_brand_lst[0][0]

    def inc_data_brand_reg(self):
        if not os.path.exists(self._inc_p):
            raise Exception("%s does not exist!" % self._inc_p)
        try:
            inc_fn = open(self._inc_p)
            idx = 0
            inc_data_lst = []
            for line in inc_fn:
                idx += 1
                if idx % 100000 == 0: self.logger.info(idx)
                line = line.strip()
                if line == "": continue

                lst1 = line.split("\t")
                if len(lst1) != 2:
                    self.logger.info("inc_data_brand_reg error data: %s" % line)
                    continue
                sid, ori_name = lst1
                sid = sid.strip()

                if sid in self._old_sid_dict: continue
                s_name = tool.s_name_dealing(ori_name)
                tmp_brand = self._brand_reg(s_name)
                if tmp_brand is None:
                    self.logger.error("brand-reg error: %s" % lst1)
                    continue
                r = "\x01".join([sid, ori_name, tmp_brand])
                inc_data_lst.append(r)

            self.logger.info("inc_data len: %s" % len(inc_data_lst))
            inc_fn.close()

            with open(self._output_p + "_inc_data_tmp", 'w') as f3:
                f3.write("\n".join(inc_data_lst))
                f3.flush()

            tmp_lst = self._old_data + inc_data_lst
            self.logger.info("total data: %s" % len(tmp_lst))
            with open(self._output_p, 'w') as f3:
                f3.write("\n".join(tmp_lst))
                f3.flush()

            self.logger.info("liwei-method changing base_file: dp_brand_result.txt.brandreg")
            time_str = time.strftime("%y-%m-%d_%H")
            shutil.copyfile(self._ori_p, self._ori_p + "_" + time_str)
            shutil.copyfile(self._output_p, self._ori_p)

            return 0
        except Exception as e:
            raise e

    def inc_data_stat(self):
        tool.brand_stat_simple(self._output_p, self._inc_data_stat)
