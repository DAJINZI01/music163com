## 网易云音乐 [https://music.163.com/](https://music.163.com/)

### 1. 分析音乐下载接口

### 1.1 根据`id`值获取榜单前100歌曲信息的接口

[https://music.163.com/#/discover/toplist?id=19723756](https://music.163.com/#/discover/toplist?id=19723756)

``` json
[{"ftype":0,"no":2,"publishTime":0,"score":100.0,"copyrightId":1416682,"mvid":0,"transNames":null,"commentThreadId":"R_SO_4_1429908253","alias":[],"privilege":{"st":0,"flag":64,"subp":1,"fl":128000,"fee":0,"dl":0,"cp":1,"preSell":false,"cs":false,"toast":false,"maxbr":999000,"id":1429908253,"pl":999000,"sp":7,"payed":0},"djid":0,"album":{"id":86399222,"name":"歌手·当打之年 第6期","picUrl":"http://p2.music.126.net/muqRnruZBkljZgnvzDzE_A==/109951164795622920.jpg","tns":[],"pic_str":"109951164795622920","pic":109951164795622920},"artists":[{"id":861777,"name":"华晨宇","tns":[],"alias":[]}],"fee":8,"type":0,"duration":319236,"status":0,"name":"神树 (Live)","id":1429908253},
```

一共是一百个数据

#### 1.2 歌词接口

[https://music.163.com/weapi/song/lyric?csrf_token=](https://music.163.com/weapi/song/lyric?csrf_token=)

这个接口是一个`post`请求，`form`表单为

```python
{
    "params": xxx,
    "encSecKey": xxx,
}
```

copy浏览器上面的这两个值，发送`post`请求拿到了数据。记下来就要考虑解析这个值了，不然不能根据歌曲来请求歌词

#### 1.3 歌曲下载连接接口

[https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=](https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=)

这个接口是一个`post`请求，`form`表单为

```python
{
    "params": xxx,
    "encSecKey": xxx,
}
```

copy浏览器上面的这两个值，发送`post`请求拿到了数据。记下来就要考虑解析这个值了，不然不能根据歌曲来请求歌词

同样要解析出参数的意义

#### 1.4 获取歌曲详细信息的接口

[https://music.163.com/weapi/v3/song/detail?csrf_token=](https://music.163.com/weapi/v3/song/detail?csrf_token=)

这个接口是一个`post`请求，`form`表单为

```python
{
    "params": xxx,
    "encSecKey": xxx,
}
```

copy浏览器上面的这两个值，发送`post`请求拿到了数据。记下来就要考虑解析这个值了，不然不能根据歌曲来请求歌词

同样要解析出参数的意义

#### 1.5 获取歌曲评论的接口

[https://music.163.com/weapi/v1/resource/comments/R_SO_4_1429908253?csrf_token=](https://music.163.com/weapi/v1/resource/comments/R_SO_4_1429908253?csrf_token=)

这个接口是一个`post`请求，`form`表单为

```python
{
    "params": xxx,
    "encSecKey": xxx,
}
```

copy浏览器上面的这两个值，发送`post`请求拿到了数据。记下来就要考虑解析这个值了，不然不能根据歌曲来请求歌词

同样要解析出参数的意义

多有的问题都在这两个地方的参数

在控制台中搜一下这两个参数，得到了:

```js
var bVj8b = window.asrsea(JSON.stringify(i7b), brx0x(["流泪", "强"]), brx0x(Xs2x.md), brx0x(["爱心", "女孩", "惊恐", "大笑"]));
e7d.data = k7d.cx8p({
    params: bVj8b.encText,
    encSecKey: bVj8b.encSecKey
})
window.asrsea = d
```

可以看出，知道`asrsea`函数是怎么工作的就解决了问题，又因为`window.asrsea = d,`所以看一下`d`函数

`d`函数又由`a/b/c`函数组成，所以，接下来一次看一下`a/b/c`函数

```js
// 产生一个随机的取自`[a-zA-Z0-9]`指定`a`长度的字符串
function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
}
```

产生一个随机的取自`[a-zA-Z0-9]`指定`a`长度的字符串

```js
/*
* 用b传进来的值作为秘钥，对a进行加密 aes
*/
function b(a, b) {
    var c = CryptoJS.enc.Utf8.parse(b) // c为秘钥, b传进来的值
    , d = CryptoJS.enc.Utf8.parse("0102030405060708") // 密钥偏移量
    , e = CryptoJS.enc.Utf8.parse(a) // 对a要加密的数据 
    , f = CryptoJS.AES.encrypt(e, c, {
        iv: d, // 密钥偏移量
        mode: CryptoJS.mode.CBC // 加密模式
    });
    return f.toString() // 加密的字符串
}
```

```js
// 应该是进行了rsa加密
function c(a, b, c) {
    var d, e;
    // 百度了一下，这个return 使用了 逗号运算符 先计算表达式1的值，再计算表达式2的值，……一直计算到表达式n的值
    return setMaxDigits(131), 
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a) // 最后返回的是e
}
```

````js
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
````

接下来看一下

```js
/*
	使用
	brx0x(["流泪", "强"])			010001
	brx0x(Xs2x.md) 						00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
	brx0x(["爱心", "女孩", "惊恐", "大笑"])		0CoJUm6Qyw8W8jud
	这里只有 i7b 是不固定的其他都是固定的，好像
*/ 
var bVj8b = window.asrsea(JSON.stringify(i7b), brx0x(["流泪", "强"]), brx0x(Xs2x.md), brx0x(["爱心", "女孩", "惊恐", "大笑"]));
i7b = {
    "logs": '[{"action":"bannerimpress","json":{"type":"10_专辑","url":"/album?id=86495711","id":"86495711","position":2}}]',
    "csrf_token": ""
}
```

