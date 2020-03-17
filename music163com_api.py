# coding=utf-8
import requests
import json
import re
import copy

from lxml import etree

from cipher import encrypt_WangYiYun
from settings import url_json


class Music163ComAPI(object):
    """music.163.com 音乐爬虫"""
    def __init__(self):
        """
        初始化方法
        """
        # 请求头
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        }

    def __get_data(self, item):
        """
        获取数据，主要做一些表单数据的加密为params和encSecKey，和发送post请求
        :param item: 要获取的数据类型
        :return: 字典数据
        """
        # 1. 转换为 严格的 json数据
        i7b = json.dumps(item["json"], ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        # 2. 进行网易云的数据加密 返回post表单数据params和encSecKey
        data = encrypt_WangYiYun(i7b)
        # data = {
        #     "params": "x0YbStcEC6xg93xRhb5/7nGs82Nsk1zi0hNDW3Ja1OQEeiWNko/UIj+jGgj1RVUgYKOa+wDLQ2cUMxcWdADaUmvKkC/DDDyHQF0P62Mi5kyw949+S/sF6GggQTITC3dJpZT48G8QGkB0c2S10/vRXw==",
        #     "encSecKey": "2788900f5ce3df5914beae8800c2f8677be41ed70839029ab2994bd66228214f78845a53c6b4e3d25ce31a50e2ca7790562f54e612dc976df5cab1796b4124771111eabd76c9d834b5579eade35f8b4cdb1fb7e42f683afddd8acaf4c76f13f70f2e359430c2c709e4275b180b99a79bc357cbd247a6a2fdbfdab359fd8f6230",
        # }
        # 3. 发送post请求，解析为字典
        response = requests.post(item["url"], headers=self.headers, data=data).json()
        # 4. 返回
        return response

    def get_lyric(self, id):
        """
        获取歌词
        :param id:  歌词id
        :return:    字符串 标准的歌词格式的文本
        """
        lyric = copy.deepcopy(url_json["lyric"])
        lyric["json"]["id"] %= id
        return self.__get_data(lyric)["lrc"]["lyric"]

    def get_player(self, id):
        """
        获取歌曲下载链接的相关信息
        :param id:  歌词id
        :return:    url字符串
        """
        player = copy.deepcopy(url_json["player"])
        player["json"]["ids"] %= id
        return self.__get_data(player)["data"][0]["url"]

    def get_comments(self, id, offset=1, limit=10):
        """
        获取歌曲下载链接的相关信息
        :param id:      歌词id
        :param offset:  偏移
        :param limit:   数量 经过测试如果数量小于10 会返回空的树
        :return:        字典对象，这里暂时不进行数据的过滤
        """
        comments = copy.deepcopy(url_json["comments"])
        comments["url"] %= id
        comments["json"]["rid"] %= id
        comments["json"]["offset"] %= offset
        comments["json"]["limit"] %= limit
        return self.__get_data(comments)

    def get_detail(self, id):
        """
        获取歌曲详细信息
        :param id: 歌曲id
        :return: 字典对象，这里不做数据过滤处理
        """
        detail = copy.deepcopy(url_json["detail"])
        detail["json"]["id"] %= id
        detail["json"]["c"] %= id
        return self.__get_data(detail)

    def get_recommend(self):
        """
        获取推荐信息
        :return:
        """
        recommend = copy.deepcopy(url_json["recommend"])
        return self.__get_data(recommend)

    def get_bang_recommend(self, id, offset=0, limit=20):
        """
        获取榜单评论
        :param id: 歌曲id
        :param offset: 偏移
        :param limit: 数量
        :return:
        """
        bang_recommend = copy.deepcopy(url_json["bang_recommend"])
        bang_recommend["url"] %= id
        bang_recommend["json"]["rid"] %= id
        bang_recommend["json"]["offset"] %= offset
        bang_recommend["json"]["limit"] %= limit
        return self.__get_data(bang_recommend)

    def search_suggest(self, s, limit=8):
        """
        关键字搜索
        :param s: 关键字
        :param limit: 数量，默认8条
        :return: 字典对象
        """
        search = copy.deepcopy(url_json["search"])
        search["json"]["s"] %= s
        search["json"]["limit"] %= limit
        return self.__get_data(search)

    def multimatch(self, s):
        """
        多匹配
        :param s: 关键字
        :return: 字典对象
        """
        match = copy.deepcopy(url_json["multimatch"])
        match["json"]["s"] %= s
        return self.__get_data(match)

    def cloud_search(self, s, offset=0, limit=30):
        """
        云搜索，歌曲
        :param s: 关键词
        :param offset: 偏移
        :param limit: 数量
        :return:
        """
        cloud = copy.deepcopy(url_json["cloudsearch"])
        cloud["json"]["s"] %= s
        cloud["json"]["offset"] %= offset
        cloud["json"]["limit"] %= limit
        return self.__get_data(cloud)

    def get_song_list(self, id):
        """
        通过id获取音乐列表
        :param id: 磅单id
        :return: 100个歌曲实例
        """
        song_list_url = "https://music.163.com/discover/toplist?id={}".format(id)
        response = requests.get(song_list_url, headers=self.headers)
        html = response.content.decode("utf-8")
        res = re.findall(r'<textarea id="song-list-pre-data" style="display:none;">(.+?)</textarea>', html)[0]
        return json.loads(res)

    def get_all_bang(self):
        """
        提取页面 https://music.163.com/discover/toplist的所有的榜单
        :return: 封装好的数据
        """
        url = "https://music.163.com/discover/toplist"
        response = requests.get(url, headers=self.headers)
        elem = etree.HTML(response.content.decode("utf-8"))
        root = elem .xpath('//div[@class="n-minelst n-minelst-2"]')[0]
        bang_list = root.xpath("./h2/text()")
        ul_list = root.xpath("./ul")
        data = {}
        for bang, ul in zip(bang_list, ul_list):
            li_list = ul.xpath("./li")
            item_list = []
            for li in li_list:
                item = {
                    "id": li.xpath('./@data-res-id')[0],
                    "name": li.xpath('.//p[@class="name"]/a/text()')[0],
                }
                item_list.append(item)
            data[bang] = item_list
        return data




if __name__ == "__main__":
    m163 = Music163ComAPI()
    # print(m163.get_lyric(1329491587))
    # print(m163.get_player(1329491587))
    # print(json.dumps(m163.get_comments(1329491587), ensure_ascii=False))
    # print(json.dumps(m163.get_detail(1329491587), ensure_ascii=False))
    # print(m163.get_recommend())
    # print(m163.search_suggest("告白气球", 2))
    # print(m163.multimatch("告白气球"))
    # print(json.dumps(m163.cloud_search("荷塘月色"), ensure_ascii=False))
    # print(json.dumps(m163.get_bang_recommend(19723756), ensure_ascii=False))
    # print(json.dumps(m163.get_song_list(19723756), ensure_ascii=False))
    print(m163.get_all_bang())

