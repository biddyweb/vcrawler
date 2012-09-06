# -*- coding: utf-8 -*-

from util import get_src, Compiled, Download

def sina_download_by_id(video_id):
    xml_url = 'http://v.iask.com/v_play.php?vid=' + video_id
    xml = get_src(xml_url)
    video_links = Compiled.sina_video_links(xml)
    Download.gets(video_links, merge=True)

def sina(url):
    html = get_src(url)
    video_id = Compiled.sina_html2id(html)
    sina_download_by_id(video_id)
