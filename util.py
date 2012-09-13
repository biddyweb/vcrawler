# -*- coding: utf-8 -*-

import re
import urllib2
import subprocess

class CONFIG(object):
    # download command
    # command = tool + url
    axel = 'axel -a -n 10 '
    downloader = axel


def decompress(data, method):
    """解压压缩过的源代码
    参考了tornado.util
    可以处理 gzip 和 deflate
    """
    assert method in ['gzip', 'deflate'], 'unable to decompress srouce'
    import zlib
    return zlib.decompress(data, zlib.MAX_WBITS+16)


def get_src(url):
    """获取页面源代码"""
    response = urllib2.urlopen(url)
    data = response.read()
    # 判断源代码是否进行了压缩
    compress = response.headers.get('Content-Encoding')
    if compress:
        data = decompress(data, compress)
    return data


def get_html(url):
    """获取页面源代码 并 整理"""
    from BeautifulSoup import BeautifulSoup
    data = get_src(url)
    return BeautifulSoup(data).prettify()


class Compiled(object):
    """预编译的正则及相关函数"""

    # bilibili 判断url是否完整 是否是单个视频
    re_bili_url = re.compile(
        r'''(?ix)
        (?P<prefix>
            https?://
            (www.bilibili.tv | bilibili.kankanews.com)
            /video/
        )?
        (?P<vid> av\d+) /?
        (?P<list> index_\d+.html)?
        ''')
    @classmethod
    def bili_url(cls, url):
        m = cls.re_bili_url.match(url)
        assert m, 'unsupported url'
        if not m.group('prefix'):
            url = 'http://www.bilibili.tv/video/' + url + '/'
        if m.group('list'):
            return (url, 'one')
        return (url, 'all')

    # bilibili 判断是否为视频列表
    re_bili_list_len = re.compile(
        r'''(?ix)
        <option [^>]+>
        [^<]+
        </option>
        ''')
    @classmethod
    def bili_list_len(cls, html):
        """返回视频列表长度
        返回0即为单个视频
        """
        m = cls.re_bili_list_len.findall(html)
        return len(m)

    # bilibili 获取视频原地址
    re_bili_source = re.compile(
        r'''(?ix)
        (?: src="https://secure.bilibili.tv/secure, | flashvars=")
        (\w{1,2}id) = ([a-z0-9=]+) "
        ''')
    @classmethod
    def bili_source(cls, html):
        m = cls.re_bili_source.search(html)
        assert m, 'video not found'
        return m.group(1), m.group(2)

    # bilibili 获取xml中的视频地址
    re_bili_video_links = re.compile(
        r'''(?ix)
        <!\[CDATA\[
        (http://[a-z0-9./?=,&;%]+)
        \]\]>
        ''')
    @classmethod
    def bili_video_links(cls, xml):
        """返回视频地址列表"""
        m = cls.re_bili_video_links.findall(xml)
        return m

class Download(object):
    """下载视频"""

    @classmethod
    def gets(cls, urls, merge=False):
        for url in urls:
            cls.get(url)

    @classmethod
    def get(cls, url):
        command = CONFIG.downloader + '"' +  url + '"'
        subprocess.call(command, shell=True)

