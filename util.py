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

    # 视频网站判断
    re_website = re.compile(
        r'''(?ix)
        https?://
        (
        (?P<bili_one> (www.bilibili.tv|bilibili.kankanews.com)/video/av\d+/index_\d+.html ) |
        (?P<bili> (www.bilibili.tv|bilibili.kankanews.com)/video/av\d+/ ) |
        (?P<qq> v.qq.com/\w+/\w/[a-z0-9.?=]+ ) |
        (?P<sina> video.sina.com.cn/[-a-z0-9./]+ )
        )
        ''')
    @classmethod
    def website(cls, url):
        """返回视频网站"""
        m = cls.re_website.match(url)
        assert m, 'unsupported url '+url
        site = None
        if m.group('bili_one'): site = 'bili_one'
        elif m.group('bili'): site = 'bili'
        elif m.group('qq'): site = 'qq'
        elif m.group('sina'): site = 'sina'
        return site

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
        (?: flashvars=" | src="https://secure.bilibili.tv/secure,)
        (\w{1,2}id) = ([a-z0-9=]+) "
        ''')
    @classmethod
    def bili_source(cls, html):
        m = cls.re_bili_source.search(html)
        assert m, 'video not found'
        return m.group(1), m.group(2)

    # sina 获取xml中的视频地址
    re_sina_video_links = re.compile(
        r'''(?ix)
        <!\[CDATA\[
        (http://[a-z0-9./?=,&;%]+)
        \]\]>
        ''')
    @classmethod
    def sina_video_links(cls, xml):
        """返回视频地址列表"""
        m = cls.re_iask_video_links.findall(xml)
        return m

    # sina 获取html中的视频id
    re_sina_html2id = re.compile(
        r'''(?ix)
        ipad_vid:'(\d{8})',
        ''')
    @classmethod
    def sina_html2id(cls, html):
        """返回视频id"""
        m = cls.re_sina_html2id.search(html)
        assert m, 'video id not found'
        return m.group(1)

    # qq 判断视频地址是否含有视频id
    re_qq_url2id = re.compile(
        r'''(?ix)
        http://v.qq.com/\w+/\w/[\w\d]+\.html\?vid=
        ([a-z0-9]{11})
        ''')
    @classmethod
    def qq_url2id(cls, url):
        """返回url中的视频id"""
        m = cls.re_qq_url2id.match(url)
        if m:
            return m.group(1)

    # qq 从视频页面获取视频id
    re_qq_html2id = re.compile(
        r'''(?ix)
        vid:" ([a-z0-9]{11}) "
        ''')
    @classmethod
    def qq_html2id(cls, html):
        """返回html中的视频id"""
        m = cls.re_qq_html2id.search(html)
        assert m, 'video id not found'
        return m.group(1)

    # qq 获取视频地址
    re_qq_video_link = re.compile(
        r'''(?ix)
        http://video.store.qq.com/\d+/[a-z0-9.?=&;]+
        ''')
    @classmethod
    def qq_video_link(cls, xml):
        m = cls.re_qq_video_link.search(xml)
        assert m, 'video not found'
        return m.group()

    # qq bilibili 下载地址
    re_qq_bili_video_link = re.compile(
        r'''(?ix)
        <!\[CDATA\[
        (http://[^\]]+)
        \]\]>
        ''')
    @classmethod
    def qq_bili_video_link(cls, xml):
        m = cls.re_qq_bili_video_link.search(xml)
        assert m, 'video not found'
        return m.group(1)

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

