import os
import datetime
from time import sleep
NUM = 20 # times of scrapy
if __name__ == '__main__':
    time_list = []
    pic_num_list = []
    for i in range(1):
    # while True:
    #     os.system("scrapy crawl url-spider")
        print("---------ith time scraping---------: ", i)
        starttime = datetime.datetime.now()
        start_file_num = len(os.listdir("./pic/full"))
        # os.system("scrapy crawl pic-spider")
        os.system("scrapy crawl pic-spider --loglevel WARNING")
        end_file_num = len(os.listdir("./pic/full"))
        endtime = datetime.datetime.now()
        duration = endtime - starttime
        total_seconds = (endtime - starttime).total_seconds()
        print("time: ", total_seconds)
        print("pic: ", end_file_num - start_file_num)
        time_list.append(total_seconds)
        pic_num_list.append(end_file_num-start_file_num)
    # # 来获取准确的时间差，并将时间差转换为秒
    # mins = total_seconds / 60
    # print("total time: ", mins)
    # file_num = len(os.listdir("./pic/full"))
    # print("file num: ", file_num)
    # print("file per min: ", file_num / mins)
    print("-------final result-----------")
    print(time_list)
    print(pic_num_list)