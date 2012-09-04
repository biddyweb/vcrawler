#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

import sys
from util import *
from sina import iask_download_by_id
from qq import qq_download_by_id

def bili_one(url, html=None):
    if not html:
        html = get_html(url)

    # 获取视频地址
    siteid = Compiled.siteid(html)
    if not siteid:
        sys.exit('... video not found')

    # 下载
    if siteid.group(1) == 'vid':
        iask_download_by_id(siteid.group(2))
    elif siteid.group(1) =='qid':
        qq_download_by_id(siteid.group(2))
    else:
        raise NotImplementedError(siteid.group(1))


def bili_all(pre, length):
    """分析视频列表，获取单个视频的页面"""
    # TODO
    # 如何解析页面

    post = 'index_{}.html'
    urls = (pre + post.format(n) for n in xrange(1, length+1))
    for url in urls:
        bili_one(url)


def bilibili(url):
    """分析页面，调用相应函数下载视频"""
    html = get_html(url)
    list_len = Compiled.option(html)
    if list_len:
        bili_all(url, list_len)
    else:
        bili_one(url, html)


def main():
    if len(sys.argv) != 2:
        sys.exit('... miss url')

    bilibili(sys.argv[1])


if __name__ == '__main__':
    main()

