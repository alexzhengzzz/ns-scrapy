import os
import datetime
from time import sleep

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    for _ in range(2):
        # os.system("scrapy crawl url-spider")
        os.system("scrapy crawl pic-spider")
    endtime = datetime.datetime.now()
    duration = endtime - starttime
    file_num = len(os.listdir("./pic/full"))
    print("total time: ", duration.seconds)
    print("file num: ", file_num)
    print("file per second: ", file_num / duration.seconds)
