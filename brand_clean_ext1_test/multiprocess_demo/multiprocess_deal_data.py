import time
# import multiprocessing
from pathos.multiprocessing import ProcessingPool as Pool
import io
import math
from extract_id import Extract_id


def deal_data(data_file,epoch):
    data_list = []
    with io.open(data_file,"r",encoding="utf-8") as f:
        for line in f:
            data_list.append(line)
    tmp_list = []
    series_data_list = []
    for i in range(epoch):
        tmp_list = data_list[math.floor(i*len(data_list)/epoch):math.floor((i+1)*len(data_list)/epoch)]
        series_data_list.append(tmp_list)

    for series_data in series_data_list:
        print(len(series_data))
    return series_data_list


def test_task(x,y):
    print(str(x) + y)

def test_multiprocess():
    x_list = [1,2,3,4,5,6,7,]
    y_list = ['1','2','3','4','5','6','7']
    epoch = 8
    pool = Pool(epoch)
    res = pool.amap(test_task,x_list,y_list)
    pool.pipe(test_task,'22','222')
    pool.close()
    pool.join()


#想传入多个参数时，还可以使用该方法将参数封装，此函数可以使用import multiprocessing as mp实现多进程
# def job(r, item):
#     (x, y) = item
#     return x * y
#
# def multicore(z):
#     x_y = list(itertools.product(range(10), range(10)))
#     pool = mp.Pool()  # 无参数时，使用所有cpu核
#     # pool = mp.Pool(processes=3) # 有参数时，使用CPU核数量为3
#     res = pool.map(func, x_y)
#     return res


if __name__ == "__main__":
    #多线程的工程项目
    # time1 = time.time()
    # data_file = "./data/adidas_1two2.txt"
    # output_file = "./data/adidas_id_.txt"
    # s_list = [[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8]]
    # epoch = 8
    # pool = Pool(epoch)
    # series_data_list = deal_data(data_file,epoch)
    # analysis_id = Extract_id(output_file)       #实际的工作任务函数
    # # analysis_id.write_id(series_data_list,output_file)
    # res = pool.map(analysis_id.write_id, s_list, series_data_list)
    # pool.close()
    # pool.join()
    # time2 = time.time()
    # print('总共耗时：' + str(time2 - time1) + 's')

    #多线程测试,可方便改成demo
    test_multiprocess()