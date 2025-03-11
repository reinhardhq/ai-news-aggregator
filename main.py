#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI News Aggregator メインスクリプト
"""

import os
import sys

# srcディレクトリをパスに追加（どのディレクトリからでも実行できるようにする）
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
