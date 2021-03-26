#!/usr/bin/env python
#coding=utf-8

import sys
import os
import shutil
import time
import tool
import traceback

from brand_recognition import BrandReg

class IncBrandReg(object):
    def __init__(self, base_folder, log_instance, bc_date):
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
        try:
            self._old_sid_dict, self._old_data = self._get_ori_brand_dict()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            raise e

        if len(self._old_data) < 1:
            raise Exception("%s data is empty!!" % brandreg_p)
        self.logger.info("using BrandReg")
        self.brand_reg = BrandReg(base_folder, log_instance)

    def _get_ori_brand_dict(self):
        if not os.path.exists(self._ori_p):
            raise Exception("%s does not exist!" % self._ori_p)
        self.logger.info("loading data: %s" % self._ori_p)
        sid_dict = {}
        old_lst = []
        with open(self._ori_p) as f2:
            for line in f2:
                try:
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
                    if len(old_lst) % 10000 == 0:
                        self.logger.info("brand_data: %s" % len(old_lst))
                except Exception as e:
                    self.logger.error(traceback.format_exc())
                    self.logger.error(line)
                    continue

        self.logger.info("len of old_data: %s" % len(old_lst))
        return sid_dict, old_lst

    def inc_data_brand_reg(self):
        if not os.path.exists(self._inc_p):
            raise Exception("%s does not exist!" % self._inc_p)
        try:
            self.logger.info("reading data %s" % self._inc_p)
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
                sid = sid.strip()     #获得取到的数据并把数据存储到一个list里面

                if sid in self._old_sid_dict: continue
                s_name = tool.s_name_dealing(ori_name)  #通过oriname获取到一种s_name,主要是去除杂质预处理
                s_tmp = "\x01".join([sid, ori_name, s_name])   #将一条数据信息拼接成一个
                r = self.brand_reg.brand_rewrite(s_tmp)
                if r is None:
                    self.logger.error("brand-reg error: %s" % lst1)
                    continue
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
            # 小时级别的备份
            self.logger.info("changing base_file: dp_brand_result.txt.brandreg")
            time_str = time.strftime("%y-%m-%d_%H")
            self.logger.info("%s -> %s" % (self._ori_p, self._ori_p + "_" + time_str))
            shutil.copyfile(self._ori_p, self._ori_p + "_" + time_str)
            self.logger.info("%s -> %s" % (self._output_p, self._ori_p))
            shutil.copyfile(self._output_p, self._ori_p)

        except Exception as e:
            raise e

    def inc_data_stat(self):
        try:
            tool.brand_stat_simple(self._output_p, self._inc_data_stat)
        except Exception as e:
            raise e




