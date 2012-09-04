#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from util import *

def iask_download_by_id(v_id):
    xml = get_xml('http://v.iask.com/v_play.php?vid=' + v_id)
    video_links = Compiled.iask_videos(xml)
    Download.gets(video_links, merge=True)

