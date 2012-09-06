# -*- coding: utf-8 -*-

from util import get_src, Compiled
from sina import sina_download_by_id
from qq import qq_download_by_id

def bili_one(url, html=None):
    if not html:
        html = get_src(url)

    # 获取视频来源
    v_site, v_id = Compiled.bili_source(html)
    # 下载
    if v_site == 'vid':
        sina_download_by_id(v_id)
    elif v_site == 'cid':
        qq_download_by_id(v_id)
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
    html = get_src(url)
    # 判断是单个视频还是视频列表
    length = Compiled.bili_list_len(html)
    if length:
        bili_all(url, length)
    else:
        bili_one(url, html)
