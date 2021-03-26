#!/usr/bin/env python
#coding=utf-8

import sys

liWeiBCCateName_Dict = {
    "huoguo":       "",
    "huazhuangpin": "",
    "yinpindian":   "",
    "kafeiting":    "",
    "shaokao":      ""
}

cateName2Dir_Dict = {
    "huoguo":           "0-1-huoguo/inc_v1",
    "huazhuangpin":     "0-2-huazhuangpin/inc_v1",
    "yinpindian":       "0-3-yinpindian/inc_v1",
    "kafeiting":        "0-4-kafeiting/inc_v1",
    "chongwu":          "1-chongwu/inc_v1",
    "shaokao":          "2-shaokao/inc_v1",
    "mianbaotiandian":  "3-mianbaotiandian/inc_v1",
    "xican":            "4-xican/inc_v1",
    "luwei":            "5-luwei/inc_v1",
    "shuiguo":          "6-shuiguo/inc_v1",
    "xiexue":           "7-xiexue/inc_v1",
    "yundonghuwai":     "8-yundonghuwai/inc_v1",
    "xiaochikuaican":   "9-00-xiaochikuaican/inc_v1",
    "meishi-qita":      "9-10-qita/inc_v1",
    "fuzhuangkuaixiao": "9-11-fuzhuangkuaixiao/inc_v1",
    "chaoshibianli":    "9-12-chaoshibianli/inc_v1",
    "jiajujiancai":     "9-13-jiajujiancai/inc_v1",
    "shumachanpin":     "9-14-shumachanpin/inc_v1",
    "zongheshangchang": "9-15-zongheshangchang/inc_v1",
    "gouwu-qita":       "9-16-gouwu-qita/inc_v1",
    "xuexipeixun":      "9-17-xuexipeixun/inc_v1",
    "liren":            "9-18-liren/inc_v1",
    "xiuxianyule":      "9-19-xiuxianyule/inc_v1",
    "yundongjianshen":  "9-20-yundongjianshen/inc_v1",
    "qinzi":            "9-21-qinzi/inc_v1",
    "jiehun":           "9-22-jiehun/inc_v1",
    "yaodian":          "9-23-yaodian/inc_v1",
    "xidihuli":         "9-24-xidihuli/inc_v1",
    "yake":             "9-25-yake/inc_v1",
    "tijianzhongxin":   "9-26-tijianzhongxin/inc_v1",
    "fuyouyiyuan":      "9-27-fuyouyiyuan/inc_v1",
    "lvxingshe":        "9-28-lvxingshe/inc_v1"
}

cateName2WhereCondition_Dict = {
    "huoguo":           "where t.category_name='火锅'",
    "huazhuangpin":     "where t.category_name='化妆品'",
    "yinpindian":       "where t.category_name='饮品店'",
    "kafeiting":        "where t.category_name='咖啡厅'",
    "chongwu":          "where t.category_name in ('宠物食品用品', '宠物店', '宠物医院', '其他宠物', '购宠')",
    "shaokao":          "where t.category_name='烧烤'",
    "mianbaotiandian":  "where t.category_name ='面包甜点'",
    "xican":            "where t.category_name ='西餐'",
    "luwei":            "where t.sub_category_name in ('熟食熏酱','熟食','卤味鸭脖')",
    "shuiguo":          "where t.category_name ='水果生鲜'",
    "xiexue":           "where t.category_name='鞋靴'",
    "yundonghuwai":     "where t.category_name='运动户外'",
    "xiaochikuaican":   "where t.category_name ='小吃快餐' and t.sub_category_name not in ('熟食熏酱','熟食','卤味鸭脖')",
    "meishi-qita":      "where t.category_name  in ('其他美食', '食品保健', '川菜', '本帮江浙菜', '江河湖海鲜', '东北菜' ,'粤菜/潮州菜', '家常菜' ,'湘菜', '日本菜', '韩国料理', '小龙虾', '北京菜', '云贵菜', '西北菜', '自助餐', '湖北菜', '福建菜', '闽菜', '东南亚菜')",
    "fuzhuangkuaixiao": "where t.sub_category_name in ('快时尚', '服装', '内衣') or t.category_name ='其他服饰鞋包'",
    "chaoshibianli":    "where t.category_name ='超市/便利店'",
    "jiajujiancai":     "where t.category_name='家居建材'",
    "shumachanpin":     "where t.sub_category_name ='数码产品'",
    "zongheshangchang": "where t.category_name ='综合商场'",
    "gouwu-qita":       "where t.channel_id=20 and t.category_name not in ('化妆品','综合商场','超市/便利店','水果生鲜','内衣','服装','鞋靴','家居建材','其他服饰鞋包') and t.sub_category_name not in ('快时尚')",
    "xuexipeixun":      "where t.channel_name='学习培训' or t.category_name in ('幼儿才艺','幼儿外语')",
    "liren":            "where t.channel_name='丽人'",
    "xiuxianyule":      "where t.channel_name='休闲娱乐'",
    "yundongjianshen":  "where t.channel_name='运动健身'",
    "qinzi":            "where t.channel_name='亲子'",
    "jiehun":           "where t.channel_name='结婚'",
    "yaodian":          "where t.category_name='药店'",
    "xidihuli":         "where t.category_name='洗涤护理'",
    "yake":             "where t.category_name='齿科'",
    "tijianzhongxin":   "where t.category_name='体检中心'",
    "fuyouyiyuan":      "where t.category_name='妇幼医院'",
    "lvxingshe":        "where t.sub_category_name='旅行社'"
}


brand_init_file_lst = ["real_brand.txt", "word_dict.txt", "error.txt", "del_brand.txt", ]
