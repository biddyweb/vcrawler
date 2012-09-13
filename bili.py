# -*- coding: utf-8 -*-

from util import get_src, Compiled, Download

def download_by_cid(video_id):
    xml_url = 'http://interface.bilibili.tv/playurl?cid=' + video_id
    xml = get_src(xml_url)
    video_links = Compiled.bili_video_links(xml)
    Download.gets(video_links)


def bili_one(url, html=None):
    if not html:
        html = get_src(url)

    # 获取视频来源
    v_site, v_id = Compiled.bili_source(html)
    # 下载
    if v_site == 'cid':
        download_by_cid(v_id)
    else:
        raise NotImplementedError(v_site + '=' +  v_id)


def bili_all(pre, length):
    """分析视频列表，获取单个视频的页面"""
    post = 'index_{}.html'
    urls = (pre + post.format(n) for n in xrange(1, length+1))
    for url in urls:
        bili_one(url)


def bilibili(url):
    """分析页面，调用相应函数下载视频"""
    url, down = Compiled.bili_url(url)
    html = get_src(url)
    if down == 'all':
        # 判断是单个视频还是视频列表
        length = Compiled.bili_list_len(html)
        if length:
            bili_all(url, length)
    bili_one(url, html)
