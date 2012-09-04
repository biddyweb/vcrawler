# -*- coding: utf-8 -*-

import re
import urllib2
import subprocess
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

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
    html = BeautifulSoup(data).prettify()
    return html

def get_xml(url):
    """获取xml文件"""
    response = urllib2.urlopen(url)
    data = response.read()
    xml = BeautifulStoneSoup(data).prettify()
    return xml

class Compiled(object):
    """预编译的正则及相关函数"""
    # bilibili 判断是否为视频列表
    re_option = re.compile(
        r'''(?ix)
        <option [^>]+>
        [^<]+
        </option>
        ''')
    @classmethod
    def option(cls, html):
        res = cls.re_option.findall(html)
        return len(res)

    # bilibili 获取视频原地址
    re_siteid = re.compile(
        r'''(?ix)
        (?: flashvars=" | src="https://secure.bilibili.tv/secure,)
        (\w{1,2}id)=([a-z0-9]+)"
        ''')
    @classmethod
    def siteid(cls, html):
        res = cls.re_siteid.search(html)
        return res

    # iask 获取视频地址
    re_iask_videos = re.compile(
        r'''(?ix)
        <!\[CDATA\[
        (http://[a-z0-9./?=,&;%]+)
        \]\]>
        ''')
    @classmethod
    def iask_videos(cls, xml):
        res = cls.re_iask_videos.findall(xml)
        return res

class Download(object):
    @classmethod
    def gets(cls, urls, merge=False):
        for url in urls:
            cls.get(url)

    @classmethod
    def get(cls, url):
        s = 'axel -n 10 "' + url + '"'
        subprocess.call(s, shell=True)

