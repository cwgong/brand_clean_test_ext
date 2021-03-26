#!/usr/bin/env python
#coding=utf-8

import sys
import os
import bc_config


for k, tmp_dir in bc_config.cateName2Dir_Dict.items():
    for tmp_file in bc_config.brand_init_file_lst:
        tmp_path = tmp_dir + "/" + tmp_file
        if not os.path.exists(tmp_path):
            print("touch %s" % tmp_path)
            fd = open(tmp_path, "w")
            fd.close()
