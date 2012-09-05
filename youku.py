# -*- coding: utf-8 -*-

import json
from time import time
from random import randint

from util import get_html, Download

def youku_download_by_id(video_id):
    # http://v.youku.com/v_show/id_{video_id}.html

#http://f.youku.com/player/getFlvPath/sid/
# 134434081131213125530_ 随机生成的，可以用00代替
# 00
# /st/
# flv 表示所要下载的视频格式，也可以选mp4，如果有的话
# /fileid/03000109
# 00
# 50201D77EDBC04650AC2DD6027D5-ED5F-27F6-8E73-DEF478121887 fileid，需要通过seed和streamfileids来破解，每段视频都一样
# &K=
# b499f3d5df944cfc2827e2ec segs中获得的，不需要破解，每段视频都不一样

    print('youku')
    print(video_id)


def youku_download_by_id2(video_id):
    info_url = 'http://v.youku.com/player/getPlayList/VideoIDS/'+video_id
    info = json.loads(get_src(info_url))['data'][0]

    segs = info['segs']
    types = segs.keys()
    for x in ['hd2', 'mp4', 'flv']:
        if x in types:
            stream_type = x
            break
    else:
        raise NotImplementedError()
    file_type = {'hd2':'flv', 'mp4':'mp4', 'flv':'flv'}[stream_type]

    seed = info['seed']
    source = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890')
    mixed = ''
    while source:
        seed = (seed * 211 + 30031) & 0xFFFF
        index = seed * len(source) >> 16
        c = source.pop(index)
        mixed += c

    ids = info['streamfileids'][stream_type].split('*')[:-1]
    vid = ''.join(mixed[int(i)] for i in ids)
    sid = '{0}{1}{1}'.format(int(time()*1000), randint(1000,1999))

    urls = []
    for s in segs[stream_type]:
        no = '{:02x}'.format(int(s['no']))
        url = 'http://f.youku.com/player/getFlvPath/sid/{}_{}/st/{}/fileid/{}{}{}?K={}&ts={}'
        url = url.format(sid, no, file_type, vid[:8], no.upper(), vid[10:], s['k'], s['seconds'])
        #urls.append((url, int(s['size'])))
        urls.append(url)

    Download.gets(urls)
