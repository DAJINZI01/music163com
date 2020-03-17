# coding=utf-8
from Crypto.Cipher import AES

import random
import codecs
import json
import base64

from test import WangYiYun as t1
from t2 import WangYiYun as t2

"""
/*
	使用
	brx0x(["流泪", "强"])                   010001
	brx0x(Xs2x.md) 						      00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
	brx0x(["爱心", "女孩", "惊恐", "大笑"])     0CoJUm6Qyw8W8jud
	这里只有 i7b 是不固定的其他都是固定的，好像
*/ 
var bVj8b = window.asrsea(JSON.stringify(i7b), brx0x(["流泪", "强"]), brx0x(Xs2x.md), brx0x(["爱心", "女孩", "惊恐", "大笑"]));
i7b = {
    logs: '[{"action":"bannerimpress","json":{"type":"10_专辑","url":"/album?id=86495711","id":"86495711","position":2}}]',
	csrf_token: ""
}
"""
PUB_KEY = b"010001"
MODULUS = b"00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
KEY = b"0CoJUm6Qyw8W8jud"
IV = b"0102030405060708"


def get_random_str(n):
    """
    产生指定n位数的随机字符串 [a-zA-Z0-9]
    :param n: 随机字符串的位数
    :return:
    """
    text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    random_str = ""
    # return "".join([random_str+random.choice(text) for i in range(n)]).encode("utf-8")
    return b"abcdefghijklmnop"


def add_to_16(text):
    """
    AES 算法要求明文的字节是16的倍数
        补足为16的倍数
    :param text: 要加密的文本
    :return:
    """
    text += b"\x01" * (16 - len(text) % 16) # 注意是 \x07 不是 \x00
    return text


def encrypt_AES(plaintext, key, iv):
    """
    AES加密
    :param plaintext: 要加密的内容都是16位的字节数据
    :param key: 密钥
    :param iv: 偏移
    :return: 二进制的密文
    """
    # 创建一个 AES 对象
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    # 加密 明文
    ciphertext = aes.encrypt(add_to_16(plaintext))
    return base64.b64encode(ciphertext)


def encrypt_RSA(plaintext, pub_key, modulus):
    """
    RSA 加密
    :param plaintext:
    :param pub_key: 公钥 010001
    :param modulus: 00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
    :return: 二进制的密文
    """
    """
    modulus =
    """
    plaintext = plaintext[::-1]
    rs = int(codecs.encode(plaintext, 'hex_codec'),
             16) ** int(pub_key, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def encrypt_WangYiYun(plaintext, pub_key=PUB_KEY, modulus=MODULUS, key=KEY):
    """
    网易云音乐加密算法
    :param plaintext: 加密的文本
    :param pub_key: RSA公钥
    :param modulus: AES
    :param key: AES密钥
    :return:
    """
    """
    /*
    * 使用d,g AES加密产生加密enctext
    * 使用e,f RSA加密产生 encSecKey
    */ 
    function d(d, e, f, g) {
        var h = {} // 对象
        , i = a(16); // 16位的随机字符串
        return h.encText = b(d, g), // g为秘钥对d进行加密
            h.encText = b(h.encText, i), // 又进行了一次加密，使用 i 16位的随机字符串
            h.encSecKey = c(i, e, f), // 使用rsa加密
            h // 最后返回 h 对象
    }
    """
    # 1. 产生16位的随机字符串
    random_16 = get_random_str(16)
    # 2. 获取encText
    encText = encrypt_AES(plaintext, key, IV)
    encText = encrypt_AES(encText, random_16, IV)
    # 3. 获取encSecKey
    encSecKey = encrypt_RSA(random_16, pub_key, modulus)
    return {"params": encText.decode("utf-8"), "encSecKey": encSecKey}


if __name__ == "__main__":
    w1 = t1()
    w2 = t2()
    # s = get_random_str(16)
    # print(s)
    # print(encrypt_AES(get_random_str(16), get_random_str(16), IV))
    # i7b = {"id": "1430652542", "c": '[{"id":"1430652542"}]', "csrf_token": ""}
    # i7b = {"ids": "[1430652542]", "level": "standard", "encodeType": "aac", "csrf_token": ""}
    # i7b = {"rid": "R_SO_4_1430652542", "offset": "0", "total": "true", "limit": "20", "csrf_token": ""}
    # i7b = {"id": "1430652542", "lv": -1, "tv": -1, "csrf_token": ""}
    # i7b = {"id": "1430652542", "c": '[{"id":"1430652542"}]', "csrf_token": ""}
    i7b = {"ids": "[1430652542]", "level": "standard", "encodeType": "aac", "csrf_token": ""}
    i7b = json.dumps(i7b, ensure_ascii=False, separators=(",",  ":")).encode("utf-8")
    # i7b_json = b'{"id":"1430652542","lv":-1,"tv":-1,"csrf_token":""}'
    # i7b_json = b'{"rid":"R_SO_4_1430652542","offset":"0","total":"true","limit":"20","csrf_token":""}'
    i7b_json = b'{"id":"1430652542","c":"[{\"id\":\"1430652542\"}]","csrf_token":""}'
    print(i7b)
    print(i7b_json)
    item = encrypt_WangYiYun(i7b)
    print(item)
    item = w1.encrypt(i7b)
    print(item)
    item = w2.encrypt(i7b)
    print(item)
    item = w2.encrypt(i7b_json)
    print(item)
