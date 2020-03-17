# coding=utf-8
# 下面这个模块是给mp4文件添加标签的，如：图片，作者，流派，还有歌词（歌词添加好像没用）什么的
from mutagen.mp4 import MP4, MP4Cover

_data = {
    # 参与创作的艺术家
    "artist": "\xa9ART",
    # 标题
    "name": "\xa9nam",
    # 发行年份
    "year": "\xa9day",
    # 唱片集
    "album": "\xa9alb",
    # 唱片集艺术家
    "album_artist": "aART",
    # 封面
    "cover": "covr",
    # 歌词
    "lyric": "\xa9lyr",
    # 流派
    "genre": "\xa9gen",
    # copyright
    "copyright": "cprt",
    # 分级
    "rtng": "content_rating",
}


def set_mp4_frames(file_name, item):
    """给mp4文件加入一些标签信息"""
    mp4 = MP4(file_name)
    for k, v in item.items():
        if k == "cover":
            mp4[_data[k]] = [MP4Cover(data=v)]
        else:
            mp4[_data[k]] = v
    mp4.save()