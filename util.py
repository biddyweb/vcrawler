# -*- coding: utf-8 -*-

import re
import urllib2
import subprocess

from BeautifulSoup import BeautifulSoup

class Configure(object):
    # download command
    # command = tool + url
    axel = 'axel -a -n 10 '
    TOOL = axel


def _decompress(data, method):
    """解压压缩过的源代码"""
    # from tornado.util
    # 可以处理 gzip 和 deflate
    import zlib
    return zlib.decompress(data, zlib.MAX_WBITS+16)


def get_html(url):
    """获取页面源代码"""
    response = urllib2.urlopen(url)
    data = response.read()
    # 判断源代码是否进行了压缩
    compress = response.headers.get('Content-Encoding')
    if compress:
        data = _decompress(data, compress)
    # 整理源代码
    data = BeautifulSoup(data).prettify()
    return data


def get_xml(url):
    """获取xml
    大都是保存下载地址的
    不用整理
    """
    response = urllib2.urlopen(url)
    return response.read()


class Compiled(object):
    """预编译的正则及相关函数"""

    # 视频网站判断
    re_website = re.compile(
        r'''(?ix)
        https?://
        (?:
        (?P<bili> (www.bilibili.tv|bilibili.kankanews.com) /video/av\d+/? ) |
        (?P<qq> v.qq.com/\w+/\w/[a-z0-9.?=]+ ) |
        (?P<sina> video.sina.com.cn/[-a-z0-9./]+ )
        )
        ''')
    @classmethod
    def website(cls, url):
        m = cls.re_website.match(url)
        site = None
        if m:
            if m.group('bili'): site = 'bili'
            elif m.group('qq'): site = 'qq'
            elif m.group('sina'): site = 'sina'
        return site

    # bilibili 判断是否为视频列表
    re_bili_option = re.compile(
        r'''(?ix)
        <option [^>]+>
        [^<]+
        </option>
        ''')
    @classmethod
    def bili_option(cls, html):
        m = cls.re_bili_option.findall(html)
        return len(m)

    # bilibili 获取视频原地址
    re_bili_siteid = re.compile(
        r'''(?ix)
        (?: flashvars=" | src="https://secure.bilibili.tv/secure,)
        (\w{1,2}id) = ([a-z0-9=]+) "
        ''')
    @classmethod
    def bili_siteid(cls, html):
        m = cls.re_bili_siteid.search(html)
        return m

    # iask 获取xml中的视频地址
    re_iask_videos = re.compile(
        r'''(?ix)
        <!\[CDATA\[
        (http://[a-z0-9./?=,&;%]+)
        \]\]>
        ''')
    @classmethod
    def iask_videos(cls, xml):
        m = cls.re_iask_videos.findall(xml)
        return [url.replace('&amp;', '&') for url in m]

    # qq 判断视频地址是否含有视频id
    re_qq_urlid = re.compile(
        r'''(?ix)
        http://v.qq.com/\w+/\w/[\w\d]+\.html\?vid=
        ([a-z0-9]{11})
        ''')
    @classmethod
    def qq_urlid(cls, url):
        m = cls.re_qq_urlid.match(url)
        return m

    # qq 从视频页面获取视频id
    re_qq_htmlid = re.compile(
        r'''(?ix)
        vid:" ([a-z0-9]{11}) "
        ''')
    @classmethod
    def qq_htmlid(cls, html):
        m = cls.re_qq_htmlid.search(html)
        return m

    # qq 获取视频地址
    re_qq_video = re.compile(
        r'''(?ix)
        http://video.store.qq.com/\d+/[a-z0-9.?=&;]+
        ''')
    @classmethod
    def qq_video(cls, xml):
        m = cls.re_qq_video.search(xml)
        return m

class Download(object):
    """下载视频"""

    @classmethod
    def gets(cls, urls, merge=False):
        for url in urls:
            cls.get(url)

    @classmethod
    def get(cls, url):
        command = Configure.TOOL + '"' +  url + '"'
        subprocess.call(command, shell=True)

