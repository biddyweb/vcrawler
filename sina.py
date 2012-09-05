#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from util import get_xml, Compiled, Download

def iask_download_by_id(video_id):
    xml_url = 'http://v.iask.com/v_play.php?vid=' + video_id
    xml = get_xml(xml_url)
    video_links = Compiled.iask_videos(xml)
    Download.gets(video_links, merge=True)

def sina(url):
    raise NotImplementedError
