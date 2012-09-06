#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

def main():
    import sys

    # 获取视频链接
    if len(sys.argv) != 2:
        sys.exit('... miss url')
    url = sys.argv[1]

    # 判断视频网站 并 调用相应程序
    from util import Compiled
    from bili import bilibili, bili_one
    from qq import qq
    from sina import sina

    download = {
        'bili_one': bili_one,
        'bili': bilibili,
        'qq': qq,
        'sina': sina,
    }

    video_site = Compiled.website(url)
    download[video_site](url)

if __name__ == '__main__':
    main()

