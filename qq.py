# -*- coding: utf-8 -*-

from util import get_src, Compiled, Download


def qq_download_by_id(video_id):
    #url = 'http://play.v.qq.com/play?vid=' + video_id
    xml_url = 'http://interface.bilibili.tv/playurl?cid=' + video_id
    xml = get_src(xml_url)
    video_link = Compiled.qq_bili_video_link(xml)
    Download.get(video_link)

def download_video(video_id):
    # 获取视频地址
    xml_url = 'http://vv.video.qq.com/geturl?vid=' + video_id
    xml = get_src(xml_url)
    video_link = Compiled.qq_video_link(xml)
    # 下载
    Download.get(video_link)

def qq(url):
    # 从url中获取视频id
    video_id = Compiled.qq_url2id(url)
    if not video_id:
        # 从html中获取视频id
        html = get_src(url)
        video_id = Compiled.qq_html2id(html)
    download_video(video_id)
