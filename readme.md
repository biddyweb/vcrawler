# vcrawler

video crawler

---------

### 目标

下载bilibili的视频

### 已完成

- bili里sina来源的视频
- qq.com的的视频

### 进行中

- bili里qq来源的视频
- bili里youku来源的视频

### 开发/运行环境

- pypy / python2.7
- package: `BeautifulSoup`
- axel

### 各种参考

- [youku-lixian](https://github.com/iambus/youku-lixian)
: 分析bilibili来源 / 下载sina视频

- [tornado](https://github.com/facebook/tornado)
: 处理gzip/deflate压缩过的网页

- [ZHANG WEIZHONG](http://www.zhangweizhong.com/2011/07/qq-video-resources-leak-problem/)
: 下载qq视频

----------

### 使用

```bash
# usage
./get_video.py [url]
```
