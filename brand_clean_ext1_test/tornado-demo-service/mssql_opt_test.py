#!/usr/bin/env python3
#coding: utf-8

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from mssql_opt import MsSqlOpt

import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filemode='a'
)

log_instance = logging.getLogger("brand_clean_logger")
log_file_name = 'log/brand_clean_log_test'
fileTimeHandler = TimedRotatingFileHandler(log_file_name, \
                                           when="D", \
                                           interval=1, \
                                           backupCount=10)
fileTimeHandler.suffix = "%Y-%m-%d.log"
formatter = logging.Formatter('%(name)-12s %(asctime)s level-%(levelname)-8s thread-%(thread)-8d %(message)s')
fileTimeHandler.setFormatter(formatter)
log_instance.addHandler(fileTimeHandler)

mssql_opt = MsSqlOpt("gouwu-qita", "2020-02-01", log_instance)
#mssql_opt.add_inc_brand_data()
'''
legal_brand_dict = mssql_opt.getting_legal_brand()

lst1 = []
for k,v in legal_brand_dict.items():
    lst1.append(k)


with open("z_gouwu_qita_legal_brand.txt", "w") as f2:
    f2.write("\n".join(lst1))
    f2.flush()
'''

mssql_opt.get_top20_data()



