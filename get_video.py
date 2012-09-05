#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

def main():
    import sys

    # 获取视频链接
    if len(sys.argv) != 2:
        sys.exit('... miss url')
    url = sys.argv[1]

    # 判断视频网站 调用相应程序
    from util import Compiled
    from bili import bilibili
    from qq import qq
    from sina import sina

    download = {
        'bili': bilibili,
        'qq': qq,
        'sina': sina,
    }
    site = Compiled.website(url)
    if site and download[site]:
        download[site](url)
    else:
        sys.exit('... unsuppoeted url')

if __name__ == '__main__':
    main()

