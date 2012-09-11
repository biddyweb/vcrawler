# vcrawler

video crawler

---------

### 目标

下载bilibili的视频

### 运行环境

- `pypy` / `python2.7`
- 使用`axel`下载 / 可自行改为`wget`

----------

### 使用

```bash
# usage
./get_video.py [url]

#./get_video.py http://www.bilibili.tv/video/av26894/
#./get_video.py http://www.bilibili.tv/video/av26894/index_2.html
#./get_video.py http://v.qq.com/xxxxxxx
```

----------


### 已完成

- bili里sina来源的视频
- bili里qq来源的视频

还是有不少问题，碰到再解决吧。

### 进行中

- bili里youku来源的视频
- qq.com的的视频
- sina.com的视频

### 各种参考

- [scskarsper](http://9ch.co//t13951,1-1.html)
- [youku-lixian](https://github.com/iambus/youku-lixian)
- [ZHANG WEIZHONG](http://www.zhangweizhong.com/2011/07/qq-video-resources-leak-problem/)

---------

sina来源的最棒了，可惜sina把视频分段了，还要自己合并，有空去搞一下……

qq本身还算好处理，虽然我不知道那个geturl那个xml是怎么找出来的……
但是bilibili的qq来源就比较麻烦了，不管是qid还是cid，我都搞不定……
目前是直接用bilibili的解析结果。

这样干脆直接用flvcd的解析结果算了……
