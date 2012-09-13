#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

import sys
from bili import bilibili

def main():
    # 获取视频链接
    if len(sys.argv) != 2:
        sys.exit('... miss url')
    url = sys.argv[1]
    # 下载
    bilibili(url)

if __name__ == '__main__':
    main()

