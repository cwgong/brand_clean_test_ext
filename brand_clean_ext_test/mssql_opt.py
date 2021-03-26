#!/usr/bin/env python3
#coding=utf-8

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import os
import traceback
import pymssql
import bc_config
import json

class MsSqlOpt(object):
    def __init__(self, cate_name, bc_date, log_instance):
        self.conn = None
        self.cursor = None
        if cate_name == "":
            raise Exception("cate_name is empty!")
        self.cate_name = cate_name

        if bc_date == "":
            raise Exception("bc_date is empty!")
        self.bc_date = bc_date

        if log_instance == None:
            raise Exception("log_instance is None")
        self.logger = log_instance

        inc_data_result = bc_config.cateName2Dir_Dict[cate_name] + "/inc_data/dp_brands_result.txt.inc." + self.bc_date
        self.inc_data_result = inc_data_result

        try:
            self.conn = pymssql.connect(server='172.21.15.61', port='1433', \
                                   user='jiangtao', password='dpbrand123!@#', \
                                   database='o2o', charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise e

    def __del__(self):
        if self.cursor != None:
            self.cursor.close()

        if self.conn != None:
            self.conn.close()

    def _del_related_data(self):
        try:
            # stp1
            '''
            del_sql = "delete from dianping_brand_shop_incre where l2='%s' and dt='%s'" % \
                      (self.cate_name, self.bc_date)
            self.logger.info("del sql: %s" % del_sql)
            self.cursor.execute(del_sql)
            self.conn.commit()
            '''
            # stp2
            del_sql_flag = "delete from dianping_brand_shop_incre_status where l2='%s' and dt='%s'" % \
                           (self.cate_name, self.bc_date)
            self.logger.info("del-flag sql: %s" % del_sql_flag)
            self.cursor.execute(del_sql_flag)
            self.conn.commit()

        except Exception as e:
            raise e

    def insert_starting_flag(self):
        try:
            insert_flag_sql = "INSERT INTO dianping_brand_shop_incre_status VALUES ('%s', '%s', %d)" % \
                              (self.cate_name, self.bc_date, 2)
            self.logger.info("insert-flag: %s" % insert_flag_sql)
            self.cursor.execute(insert_flag_sql)
            self.conn.commit()
        except Exception as e:
            raise e

    def _update_inc_status(self, flag_status):
        try:
            update_flag_sql = "update dianping_brand_shop_incre_status set status=%d  where l2='%s' and dt='%s'" % \
                              (flag_status, self.cate_name, self.bc_date)
            self.logger.info("update-flag: %s" % update_flag_sql)
            self.cursor.execute(update_flag_sql)
            self.conn.commit()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            raise e

    def insert_successful_flag(self):
        self.logger.info("adding inc-brand successful!")
        self._update_inc_status(1)

    def insert_failture_flag(self):
        self.logger.info("adding inc-brand failture!")
        self._update_inc_status(0)

    def getting_legal_brand(self):
        try:
            legal_brand_dict = {}
            sel_sql = "select s.brand brand ,b.code code from dianping_brand_combine b join dianping_search_brand s on b.l1=s.l1  and b.l2=s.l2 where b.l1 in (select  l1 from dianping_brand_combine where code='%s')" % self.cate_name
            self.logger.info("getting legal-brand: %s" % sel_sql)
            self.cursor.execute(sel_sql)
            row = self.cursor.fetchall()
            self.logger.info("getting_legal_brand")
            for data in row:
                #self.logger.info(data[0])
                legal_brand_dict[data[0]] = data[1]
                #tmp = bytes(bytearray(data[0],  encoding='utf-8'))
                #legal_brand_dict[tmp] = data[1]
            if len(legal_brand_dict) == 0:
                err_s = "legal_brand_set is empty!"
                self.logger.error(err_s)
                raise Exception(err_s)
            self.logger.info("legal_brand length: %s" % len(legal_brand_dict))
            return legal_brand_dict
        except Exception as e:
            raise e

    def add_inc_brand_data(self):
        try:
            if not os.path.exists(self.inc_data_result):
                raise Exception("%s does not exsit!" % self.inc_data_result)
            self.logger.info("opt file: %s " % self.inc_data_result)
            # stp2 getting legal-brand
            try:
                legal_brand_dict = self.getting_legal_brand()
            except Exception as e:
                raise e
            # stp3
            insert_sql = "INSERT INTO dianping_brand_shop_incre VALUES (%d, %s, %s, %s, %s)"
            insert_lst = []
            insert_num = 0
            with open(self.inc_data_result) as f1:
                for line in f1:
                    line = line.strip()
                    if line == "": continue
                    lst2 = line.split("\x01")
                    if len(lst2) != 3:
                        self.logger.error("cate_name: %s err_line: %s" % (self.cate_name, lst2))
                        continue
                    lst2 = [tmp.strip() for tmp in lst2]
                    shop_id, shop_name, brand = lst2
                    #byte_brand = bytes(bytearray(brand, encoding='utf-8'))
                    #if byte_brand not in legal_brand_dict:
                    if brand not in legal_brand_dict:
                        #self.logger.info("insert brand: %s" % brand)
                        continue
                    tmp_code = legal_brand_dict[brand]
                    #self.logger.info(insert_sql % (int(shop_id), brand, '', tmp_code, self.bc_date))
                    
                    insert_lst.append((int(shop_id), brand, '', tmp_code, self.bc_date))
                    if len(insert_lst) >= 1000:
                        try:
                            # self.cursor.executemany(insert_sql, insert_lst)
                            # self.conn.commit()
                            insert_num += len(insert_lst)
                            insert_lst = []
                            self.logger.info("insert data-num: %s" % insert_num)
                        except Exception as e:
                            self.logger.error(traceback.format_exc())
                            raise e

            with open("./cursor_brand_data.txt", "a", encoding='utf-8') as f:
                # f.write(insert_lst)
                json.dump(insert_lst, f,ensure_ascii=False)

            if len(insert_lst) > 0:
                try:
                    self.cursor.executemany(insert_sql, insert_lst)
                    self.conn.commit()
                    insert_num += len(insert_lst)
                    insert_lst = []
                    self.logger.info("insert data-num: %s" % insert_num)
                except Exception as e:
                    self.logger.error(traceback.format_exc())
                    raise e
            # stp4
            # self.insert_successful_flag()

            return 0
        except Exception as e:
            self.logger.error(traceback.format_exc())
            raise e
    
    def get_top20_data(self):
        try:
            legal_brand_dict = {}
            sel_sql = "select top 20 shop_id,brand from dianping_brand_shop_incre where dt='2020-02-01'"
            self.logger.info("getting top-20 spu: %s" % sel_sql)
            self.cursor.execute(sel_sql)
            row = self.cursor.fetchall()
            for data in row:
                #self.logger.info(data[0])
                #legal_brand_dict[data[0]] = data[1]
                #print(data[1].decode("utf-8").encode("utf-8"))
                print(data[1])
                #tmp = bytes(bytearray(data[0],  encoding='utf-8'))
                #legal_brand_dict[tmp] = data[1]
            '''
            if len(legal_brand_dict) == 0:
                err_s = "legal_brand_set is empty!"
                self.logger.error(err_s)
                raise Exception(err_s)
            '''
            self.logger.info("legal_brand length: %s" % len(legal_brand_dict))
            return legal_brand_dict
        except Exception as e:
            raise e
