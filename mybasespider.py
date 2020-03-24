# coding=utf-8
import requests
import time


class MyBaseSpider(object):
    """自定义爬虫基类"""
    def __init__(self, my_log_file_name="my.log"):
        # 请求头
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }
        # 日志文件
        self.f = open(my_log_file_name, "w")

    def __del__(self):
        self.f.close()

    def my_log(self, msg):
        """记录一些日志信息"""
        self.f.write("[{}] {}\n".format(time.strftime("%Y/%m/%D %H:%M:%S", time.localtime()), msg))
        self.f.flush()

    def my_get(self, url, stream=False):
        """用于发送get请求的函数，可以处理一些反爬，还有打印一些信息"""
        response = requests.get(url, headers=self.headers, stream=stream)
        print("{} [{}]".format(response.url, response.status_code))
        return response
