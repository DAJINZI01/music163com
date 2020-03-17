import os
# 项目的根路径
BASE_DIR = "./data"
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

# 下载歌曲的并发数量
DOWNLOAD_M4A_NUM = 10

# 对应 url 发送的json数据
url_json = {
    # 歌词的json数据格式
    "lyric": {
        "url": "https://music.163.com/weapi/song/lyric?csrf_token=",
        "json": {"id": "%d", "lv": -1, "tv": -1, "csrf_token": ""},  # 529823971
    },
    # 歌曲的接口 这个接口还是网上找的 页面里面好像不用这个接口了
    "player": {
        "url": "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=",
        "json": {"ids": "[%d]", "level": "standard", "encodeType": "aac", "csrf_token": ""},
        # "url": "http://music.163.com/weapi/song/enhance/player/url?csrf_token=",
        # "json": {"ids": "[%d]", "br":128000, "csrf_token": ""}, # "[1429908253]"
    },
    # 评论的接口
    "comments": {
        "url": "https://music.163.com/weapi/v1/resource/comments/R_SO_4_%d?csrf_token=",
        "json": {"rid": "R_SO_4_%d", "offset": "%d", "total": "true", "limit": "%d", "csrf_token": ""},
    },
    # 获取歌曲详细信息的接口
    "detail": {
        "url": "https://music.163.com/weapi/v2/song/detail?csrf_token=",
        "json": {"id": "%d", "c": '[{"id":"%d"}]', "csrf_token": ""},
    },
    # 推荐
    "recommend": {
        "url": "https://music.163.com/weapi/discovery/recommend/resource?csrf_token=",
        "json": {"csrf_token": ""},
    },
    # 搜索
    "search": {
        "url": "https://music.163.com/weapi/search/suggest/web?csrf_token=",
        "json": {"s": "%s", "limit": "%d", "csrf_token": ""},
    },
    # 获取榜单的评论信息
    "bang_recommend": {
        "url": "https://music.163.com/weapi/v1/resource/comments/A_PL_0_%d?csrf_token=",
        "json": {"rid": "A_PL_0_%d", "offset": "%d", "total": "true", "limit": "%d", "csrf_token": ""},
    },
    # 多匹配 歌手
    "multimatch": {
        "url": "https://music.163.com/weapi/search/suggest/multimatch?csrf_token=",
        "json": {"s": "%s", "csrf_token": ""},
    },
    # 云搜索
    "cloudsearch": {
        "url": "https://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
        "json": {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "id": "6452", "s": "%s", "type": "1", "offset": "%d", "total": "true", "limit": "%d", "csrf_token": ""},
    },
    # 反馈的接口 没人用吧 调试挺烦人的动不动就跳出来
    "weblog": {
        "url": "https://music.163.com/weapi/feedback/weblog?csrf_token=",
        "json": {
            "logs": '[{"action":"play","json":{"type":"song","wifi":0,"download":0,"id":1429908253,"time":7,"end":"interrupt"}}]',
            # "[{"action":"play","json":{"type":"song","wifi":0,"download":0,"id":1390066209,"time":89,"end":"interrupt","source":"toplist","sourceId":"19723756"}}]"
            # '[{"action":"bannerimpress","json":{"type":"1_歌曲","url":"/song?id=1400259397","id":"1400259397","position":7}}]'
            "csrf_token": "",
        }
    },
    # 
    "p2p": {
        "url": "https://music.163.com/weapi/activity/p2p/flow/switch/get?csrf_token=",
        "json": {"csrf_token": ""}
    },
    # flow switch
    "flow": {
        "url": "https://music.163.com/weapi/activity/p2p/flow/switch/get?csrf_token=",
        "json": {"csrf_token": ""}
    }

}
