# -*- coding: utf-8 -*-

from util import get_html, get_xml, Compiled, Download


def qq_download_by_id(video_id):
    pass

def qq_download_by_id2(video_id):
    # 获取视频地址
    xml_url = 'http://vv.video.qq.com/geturl?vid=' + video_id
    xml = get_xml(xml_url)
    video_link = Compiled.qq_video(xml)
    if video_link:
        Download.get(video_link.group())

def qq(url):
    # 从url中获取视频id
    video_id = Compiled.qq_urlid(url)
    if not video_id:
        # 从html中获取视频id
        html = get_html(url)
        video_id = Compiled.qq_htmlid(html)
    assert video_id
    qq_download_by_id2(video_id.group(1))
