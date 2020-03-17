# coding=utf-8
from gevent import monkey; monkey.patch_all()
from gevent import pool

from settings import BASE_DIR, DOWNLOAD_M4A_NUM
from music163com_api import Music163ComAPI
from mybasespider import MyBaseSpider
from myutils.mp4_frame import set_mp4_frames
from myutils.mydownloader import Downloader

import os
import json
import time
import requests
import re
import queue


class Music163Com(MyBaseSpider):
    """网易云音乐歌曲爬虫"""
    def __init__(self):
        """
        初始化方法
        """
        MyBaseSpider.__init__(self)
        # api 调用
        self.api = Music163ComAPI()
        # 自定义的下载器
        self.downloader = Downloader()
        # 协程池
        self.pool = pool.Pool()
        # 歌曲队列
        self.m4a_q = queue.Queue()
        # 榜单池
        self.bang_pool = pool.Pool()

    def download_mp3(self, folder, id):
        """
        根据song下载音乐
        :param folder: 指定存放的文件夹
        :param id: 歌曲id
        :return: 下载的文件名
        """
        # 1. 创建文件夹
        mp3_folder = "{}/{}".format(BASE_DIR, folder)
        if not os.path.exists(mp3_folder):
            os.mkdir(mp3_folder)
        # print(json.dumps(song, ensure_ascii=False))
        # 2. 获取歌曲实例
        song = self.api.get_detail(id)["songs"][0]
        # 3. 判断文件是否存在
        file_name = "{}/{}.m4a".format(mp3_folder, song["name"])
        if os.path.exists(file_name):
            print("[{}] already exists.".format(file_name))
            return file_name
        # 4. 获取下载的url
        download_url = self.api.get_player(song["id"])
        # 如果 download_url 不存在
        if not download_url:
            print("[{} {} {}] download url is none".format(song["id"], song["name"], song["ar"][0]["name"]))
            return
        # 5. 下载文件
        self.downloader.download(file_name, download_url)
        # 6. 设置m4a标签
        item = {
            "name": song["name"],
            "artist": song["ar"][0]["name"],
            "album": song["al"]["name"],
            "album_artist": song["ar"][0]["name"],
            "cover": requests.get(song["al"]["picUrl"], headers=self.headers).content,
            "genre": str(song["ftype"]),
            "copyright": str(song["copyright"]),
            "year": time.strftime("%Y", time.localtime(song["publishTime"]/1000)),
            "lyric": self.api.get_lyric(song["id"]), # 说明，这里添加的歌词不支持滚动，但还是加上吧
        }
        try:
            set_mp4_frames(file_name, item)
        except:
            pass
        return file_name

    def download_lyric(self, file_name, id):
        """
        下载歌词
        :param file_name: 歌词存放的文件
        :param id: 歌曲id
        :return: 下载的文件名
        """
        # 1. 判断文件是否存在
        if os.path.exists(file_name):
            print("[{}] already exists.".format(file_name))
            return file_name
        # 2. 打开文件
        f = open(file_name, "w", encoding="utf-8")
        # 3. 写入内容
        f.write(self.api.get_lyric(id))
        # 4. 关闭文件
        f.close()
        print("[{}] download successfully.".format(file_name))
        return file_name

    def download_mp3_with_lyric(self, folder, id):
        """
        下载歌曲和歌词
        :param folder: 文件存放的位置
        :param song: 歌曲实例
        :return:
        """
        m4a_name = self.download_mp3(folder, id)
        # 如果下载连接不存在，没有下载m4a文件，退出
        if not m4a_name:
            return
        file_name = re.sub(r"(.*)\.m4a", r"\1.lrc", m4a_name)
        self.download_lyric(file_name, id)

    def download_mp3_with_lyric_async(self, folder):
        """
        异步下载歌曲和文件
        :param folder: 下载存放的文件位置
        :return:
        """
        while True:
            id = self.m4a_q.get()
            self.download_mp3_with_lyric(folder, id)
            self.m4a_q.task_done()
            if self.m4a_q.empty():
                break

    def download_mp3_by_name(self, folder, name, artist=None, lyric=False):
        """
        通过指定名字下载歌曲
        :param folder: 指定存放的文件夹
        :param name: 歌曲名字
        :param artist: 歌手, 默认可以不传入
        :param lyric: 是否下载歌词
        :return:
        """
        # 获取要下载歌曲的id
        songs = self.api.cloud_search(name)["result"]["songs"]
        # 判断是否下载歌词
        download_mp3_func = self.download_mp3_with_lyric if lyric else self.download_mp3
        # 如果没有传入artist，默认为第一个歌曲
        if not artist:
            return download_mp3_func(folder, songs[0]["id"])

        founded = False
        for song in songs:
            for ar in song["ar"]:
                if ar["name"].find(artist) != -1:
                    founded = True
                    break
            if founded:
                return download_mp3_func(folder, song["id"])
        print("[{} {}] not found.".format(name, artist))

    def download_one_bang(self, folder, id):
        """
        下载一个榜单的歌曲（100首）
        :param folder: 存放的文件夹
        :param id: 获取榜单的id
        :return:
        """
        start_time = time.time()
        # 1. 创建文件夹
        bang_folder = "{}/{}".format(BASE_DIR, folder)
        if not os.path.exists(bang_folder):
            os.mkdir(bang_folder)
        # 2. 开启并发
        for _ in range(DOWNLOAD_M4A_NUM):
            self.pool.apply_async(func=self.download_mp3_with_lyric_async, args=(folder,))
        # 3. 获取榜单数据
        song_list = self.api.get_song_list(id)
        for song in song_list:
            # self.download_mp3_with_lyric(folder, song["id"])
            self.m4a_q.put(song["id"])
        # 4. 等待结束
        self.m4a_q.join() # 阻塞等待队列为空，任务完成
        self.pool.join() # 阻塞，等待协程结束
        use_time = time.time() - start_time
        self.my_log("download bang %s use time %.2fs = %.2fm = %.2fh" % (folder, use_time, use_time/60, use_time/3600))

    def download_all_bang_menu(self):
        bang_menu_list = self.api.get_all_bang()
        # 统计时间 开始时间
        start_time = time.time()
        for bang_menu_name, bang_list in bang_menu_list.items():
            # 1. 创建文件夹
            bang_menu_folder = "{}/{}".format(BASE_DIR, bang_menu_name)
            if not os.path.exists(bang_menu_folder):
                os.mkdir(bang_menu_folder)
            # 2. 遍历所有的榜单
            for bang in bang_list:
                bang_folder = "{}/{}".format(bang_menu_name, bang["name"])
                # self.bang_pool.(self.download_one_bang, args=(bang_folder, bang["id"]))
                self.download_one_bang(bang_folder, bang["id"])

        # 3. 等待协程池结束
        # self.bang_pool.join()
        # 统计时间 结束时间
        use_time = time.time() - start_time
        self.my_log("download all bang use time %.2fs = %.2fm = %.2fh" % (use_time, use_time/60, use_time/3600))


if __name__ == '__main__':
    m = Music163Com()
    # m.download_mp3_by_name("search", "麻雀", lyric=True)
    # m.download_mp3("test", 1409154856)
    # m.download_mp3_with_lyric("test", 1409154856)
    # m.download_lyric("test.lrc", 1409154856)
    # m.download_one_bang("test", 19723756)
    m.download_all_bang_menu()
