#!/usr/bin/env python3
#coding=utf-8

import sys
import os
import tool
import re

class BrandRegBasic(object):
    def __init__(self, base_folder, log_instance):
        if not os.path.exists(base_folder):
            raise Exception("%s does not exists!" % base_folder)
        self._real_brand_p = base_folder + "/real_brand.txt"
        if not os.path.exists(self._real_brand_p):
            raise Exception("%s does not exists!" % self._real_brand_p)
        # 注：word_dict.txt和error.txt是一样的功能
        #    都是品牌改写，数据格式也一样
        self._error_p = base_folder + '/error.txt'
        if not os.path.exists(self._error_p):
            raise Exception("%s does not exists!" % self._error_p)
        self._word_dict_p = base_folder + '/word_dict.txt'
        if not os.path.exists(self._word_dict_p):
            raise Exception("%s does not exists!" % self._word_dict_p)
        self._del_brand_p = base_folder + '/del_brand.txt'
        if not os.path.exists(self._del_brand_p):
            raise Exception("%s does not exists!" % self._del_brand_p)
        # self._real_brand_Eng_p = base_folder + "/real_brand_Eng.txt"
        # if not os.path.exists(self._real_brand_Eng_p):
        #     raise Exception("%s does not exists!" % self._real_brand_Eng_p)
        self.logger = log_instance
        self.logger.info("get_real_brand")
        self.real_brand_set = self._get_real_brand()
        # self.real_brand_Eng_set = self._get_real_brand_Eng()
        self.logger.info("get_exchange_brand_pair")
        self.exchange_brand_pair = self._get_exchange_brand_pair()
        self.logger.info("get_del_brand")
        self.del_brand_dict = self._get_del_brand()

    #通过真实品牌这个文件获取到真实品牌的元组
    def _get_real_brand(self):
        # 根据real_brand进行品牌确定
        if not os.path.exists(self._real_brand_p):
            raise Exception("%s does not exist!" % self._real_brand_p)

        real_brand_set = set()
        with open(self._real_brand_p) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                real_brand_set.add(line)

        self.logger.info("len of real_brand: %s" % len(real_brand_set))
        return real_brand_set

    # def _get_real_brand_Eng(self):
    #     if not os.path.exists(self._real_brand_Eng_p):
    #         raise Exception("%s does not exist!" % self._real_brand_Eng_p)
    #
    #     _real_brand_Eng_p = set()
    #     with open(self._real_brand_Eng_p) as f1:
    #         for line in f1:
    #             line = line.strip()
    #             if line == "": continue
    #             _real_brand_Eng_p.add(line)
    #
    #     self.logger.info("len of real_brand_Eng: %s" % len(_real_brand_Eng_p))
    #     return _real_brand_Eng_p

    # no-using
    def _brand_pair_correction(self, exchange_dict, conflict_brand_set):
        # Tips: {1:2, 2:3, 3:4}这种情况会有错误

        tmp_dict = {}
        for k, v in exchange_dict.items():
            if k in conflict_brand_set:
                right_brand = exchange_dict[k]
                for k1, v1 in exchange_dict.items():
                    if v1 == k:
                        tmp_dict[k1] = right_brand

        exchange_dict_ext = {}
        for k2, v2 in exchange_dict.items():
            if k2 == v2: continue
            if k2 in conflict_brand_set: continue
            if k2 in tmp_dict:
                exchange_dict_ext[k2] = tmp_dict[k2]
            else:
                exchange_dict_ext[k2] = v2

        return exchange_dict_ext

    def _brand_pair_checking(self, exchange_dict):
        s1 = set(list(exchange_dict.keys()))
        s2 = set(list(exchange_dict.values()))
        s3 = s1 & s2
        if len(s3) > 0:
            self.logger.error("exchang-brand-pair has error, error brands is: %s" % "\t".join(list(s3)))
            return False, s3
        else:
            return True, None

    def _get_exchange_brand_pair(self):
        exchange_dict = {}
        def _line_deal(line):
            line = line.strip()
            if line == "": return
            lst1 = line.split("|")
            if len(lst1) != 2:
                self.logger.info("wrong brand pair: %s" % line)
                return
            lst1 = [z.strip() for z in lst1]
            if lst1[0] != lst1[1]:
                exchange_dict[lst1[0]] = lst1[1]

        # 根据品牌确定的结果+error.txt获得需要修正的sname结果
        if not os.path.exists(self._error_p):
            self.logger.info("%s does not exist!" % self._real_brand_p)
        else:
            with open(self._error_p) as f1:
                for line in f1:
                    _line_deal(line)
            self.logger.info("len of exchang_brand_pair: %s" % len(exchange_dict))

        if not os.path.exists(self._word_dict_p):
            self.logger.info("%s does not exist!" % self._real_brand_p)
        else:
            with open(self._word_dict_p) as f1:
                for line in f1:
                    _line_deal(line)
            self.logger.info("len of exchang_brand_pair: %s" % len(exchange_dict))

        # 品牌对检测
        chk_flag, conflict_brand_set = self._brand_pair_checking(exchange_dict)
        if not chk_flag:
            err_s = "exchang-brand-pair error: %s" % "\t".join(list(conflict_brand_set))
            self.logger.error(err_s)
            raise Exception(err_s)
        
        return exchange_dict

    def _get_del_brand(self):
        if not os.path.exists(self._del_brand_p):
            raise Exception("%s does not exist!" % self._real_brand_p)

        del_dict = {}
        with open(self._del_brand_p) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                del_dict[line] = 0
        self.logger.info("len of del_brand: %s" % len(del_dict))
        return del_dict

class BrandReg(BrandRegBasic):
    def __init__(self, base_folder, log_instance, input_lst=None):
        super(BrandReg, self).__init__(base_folder, log_instance)
        input_file = base_folder + "/dp_brands_result.txt"
        if not os.path.exists(input_file):
            raise Exception("%s does not exist!" % input_file)

        output_file = base_folder + "/dp_brands_result.txt.brandreg"
        self._input_p = input_file
        self._input_lst = input_lst
        self._output_p = output_file

    def _brand_exchange(self, ori_brand):
        if ori_brand in self.exchange_brand_pair:
            return self.exchange_brand_pair[ori_brand]
        else:
            return ori_brand

    def brand_reg(self):
        stp1_lst = []
        idx = 0
        if self._input_lst != None and len(self._input_lst) > 0:
            self.logger.info("增量数据处理")
            for line in self._input_lst:
                idx += 1
                if idx % 10000 == 0: self.logger.info(idx)
                line = line.strip()
                r = self.brand_rewrite(line)
                if r is None: continue
                stp1_lst.append(r)
        elif os.path.exists(self._input_p):
            f_input = open(self._input_p)
            for line in f_input:
                idx += 1
                if idx % 100000 == 0: self.logger.info(idx)
                line = line.strip()
                r = self.brand_rewrite(line)
                if r is None: continue
                stp1_lst.append(r)

            f_input.close()
        else:
            raise Exception("输入增量数据为空！！！")

        if len(stp1_lst) < 1:
            raise Exception("增量数据处理后数据为空！！！")

        with open(self._output_p, 'w') as f3:
            f3.write("\n".join(stp1_lst))
            f3.flush()

    def is_own_Eng(self,strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return True
        return False

    def judge_brand_Eng_(self,s_name):
        ex_brand = self._real_brand_Eng_reg_(s_name)
        tmp_brand = ex_brand if ex_brand != None else s_name
        s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))  # 去除中文字符
        s_name_list = s_name_.split(" ")
        for item in s_name_list:
            item_ = item.lower()
            if tmp_brand in item_ and len(tmp_brand) < len(item_):
                return s_name
        return tmp_brand

    def judge_brand_Eng(self, s_name):
        ex_brand = self._real_brand_Eng_reg_(s_name)
        tmp_brand = ex_brand if ex_brand != None else s_name  # 在real_word中匹配到了就令品牌为匹配到的词，否则为店铺名
        s_name_ = ''.join(filter(lambda c: ord(c) < 256, s_name))  # 去除中文字符

        s_name_merge = s_name_.replace(" ", "")  # 多个词组成的品牌店铺名合并
        tmp_brand_merge = tmp_brand.replace(" ", "")

        ahead_rgx = re.compile("^{0}".format(tmp_brand_merge))
        behind_rgx = re.compile("{0}$".format(tmp_brand_merge))
        ahead_rgx_result = ahead_rgx.search(s_name_merge)
        behind_rgx_result = behind_rgx.search(s_name_merge)

        if ahead_rgx_result != None or behind_rgx_result != None:
            return tmp_brand
        else:
            return s_name

    def _real_brand_reg(self, s_name):
        tmp_brand = None
        """
        attention: 这一步可能出现问题, 
              比如：东方骆驼，骆驼， 
              在real_brand.txt文件中，如果【骆驼】出现在【东方骆驼】前面，
              那么将导致【东方骆驼】变为【骆驼】
        """
        for r_b in self.real_brand_set:
            lst5 = s_name.split(r_b)
            if len(lst5) > 1:
                tmp_brand = r_b
                break

        return tmp_brand

    def _real_brand_reg_(self, s_name):
        tmp_brand = None
        """
        attention: 这一步可能出现问题, 
              比如：东方骆驼，骆驼， 
              在real_brand.txt文件中，如果【骆驼】出现在【东方骆驼】前面，
              那么将导致【东方骆驼】变为【骆驼】
        """
        tmp_brand_list = []
        for r_b in self.real_brand_set:
            lst5 = s_name.split(r_b)
            if len(lst5) > 1:
                tmp_brand_list.append(r_b)


        if len(tmp_brand_list) == 0:
            return None
        longest_item = tmp_brand_list[0]
        if len(tmp_brand_list) == 1:
            return longest_item

        for item in tmp_brand_list:
            if len(longest_item) < len(item):
                longest_item = item
            else:
                continue

        return longest_item

    def _real_brand_Eng_reg_(self,s_name):

        tmp_brand_list = []
        for r_b in self.real_brand_Eng_set:
            lst5 = s_name.split(r_b)
            if len(lst5) > 1:
                tmp_brand_list.append(r_b)

        if len(tmp_brand_list) == 0:
            return None
        longest_item = tmp_brand_list[0]
        if len(tmp_brand_list) == 1:
            return longest_item

        for item in tmp_brand_list:
            if len(longest_item) < len(item):
                longest_item = item
            else:
                continue

        return longest_item

    def brand_rewrite(self, line):
        line = line.strip()
        if line == "":
            self.logger.info("empty string!!")
            return None
        lst1 = line.split("\x01")
        if len(lst1) == 3:
            s_id, ori_name, s_brand = lst1  #取到相关的数据
            s_brand = s_brand.strip()
        else:
            self.logger.info("brand_rewrite error data: %s" % line)
            return None

        s_name = tool.s_name_dealing(ori_name)
        if self.is_own_Eng(s_name) == True:
            if len(self.real_brand_Eng_set) > 0:
                if s_brand not in self.real_brand_Eng_set:
                    tmp_brand = self.judge_brand_Eng(s_name)
                else:
                    tmp_brand = s_brand
            else:
                tmp_brand = s_brand

        else:
            if len(self.real_brand_set) > 0:
                if s_brand not in self.real_brand_set:
                    ex_brand = self._real_brand_reg_(s_name)     #匹配过程。如果取到的数据当中没有在数据集中找到相同的品牌，则对这种数据处理一下，在一个数据集中去匹配，进行品牌的归并
                    tmp_brand = ex_brand if ex_brand != None else s_brand   #如果对处理过的品牌就赋值给tmp_brand,否则直接赋值
                else:
                    tmp_brand = s_brand     #如果在数据集中找到了直接赋值,认为该品牌数值合比较标准

            else:
                tmp_brand = s_brand     #如果没有数据集就直接赋值
        # brand 修正
        r_brand = self._brand_exchange(tmp_brand)
        # 错误品牌检测
        if r_brand in self.del_brand_dict:
            r_brand = s_name

        return "\x01".join([s_id, ori_name, r_brand])   #拼接后返回结果

# def _real_brand_reg_(real_brand_set,s_name):
#     tmp_brand = None
#     """
#     attention: 这一步可能出现问题,
#           比如：东方骆驼，骆驼，
#           在real_brand.txt文件中，如果【骆驼】出现在【东方骆驼】前面，
#           那么将导致【东方骆驼】变为【骆驼】
#     """
#     tmp_brand_list = []
#     for r_b in real_brand_set:
#         lst5 = s_name.split(r_b)
#         if len(lst5) > 1:
#             tmp_brand_list.append(r_b)
#
#     if len(tmp_brand_list) == []:
#         return None
#
#     longest_item = tmp_brand_list[0]
#
#     if len(tmp_brand_list) == 1:
#         return longest_item
#
#     for item in tmp_brand_list:
#         if len(longest_item) < len(item):
#             longest_item = item
#         else:
#             continue
#
#     return longest_item

if __name__ == "__main__":
    # real_brand_set = ["东方骆驼","沙漠骆驼","骆驼","沙漠东方骆驼"]
    # longest_item = _real_brand_reg_(real_brand_set,"北京大沙东方骆驼")
    # print(longest_item)
    pass






