#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hacker Newsからのデータ収集モジュール
"""

import logging
import requests
from typing import List, Dict, Any
import time

logger = logging.getLogger(__name__)

class HackerNewsCollector:
    """Hacker Newsからニュースを収集するクラス"""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    ITEM_URL = f"{BASE_URL}/item"
    TOP_STORIES_URL = f"{BASE_URL}/topstories.json"
    NEW_STORIES_URL = f"{BASE_URL}/newstories.json"
    
    def __init__(self, max_items: int = 100):
        """
        コンストラクタ
        
        Args:
            max_items: 収集する最大アイテム数
        """
        self.max_items = max_items
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Hacker Newsからニュースを収集する
        
        Returns:
            収集したニュースのリスト
        """
        logger.info("Hacker Newsからニュースの収集を開始")
        
        try:
            # 最新および人気のストーリーIDを取得
            top_story_ids = self._get_story_ids(self.TOP_STORIES_URL)
            new_story_ids = self._get_story_ids(self.NEW_STORIES_URL)
            
            # 重複を除去して結合
            combined_ids = list(dict.fromkeys(top_story_ids + new_story_ids))
            
            # 最大アイテム数に制限
            story_ids = combined_ids[:self.max_items]
            logger.info(f"{len(story_ids)}件のストーリーIDを取得しました")
            
            # 各ストーリーの詳細情報を取得
            stories = []
            for story_id in story_ids:
                try:
                    story = self._get_item(story_id)
                    if story and 'url' in story and story.get('type') == 'story':
                        stories.append({
                            'title': story.get('title', ''),
                            'url': story.get('url', ''),
                            'content': story.get('text', ''),
                            'source': 'Hacker News',
                            'score': story.get('score', 0),
                            'timestamp': story.get('time', 0),
                            'comments_count': story.get('descendants', 0),
                            'hn_id': story_id
                        })
                    # APIレート制限を避けるための短い待機
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"ストーリーID {story_id} の取得中にエラーが発生しました: {str(e)}")
            
            logger.info(f"Hacker Newsから{len(stories)}件のニュースを収集しました")
            return stories
            
        except Exception as e:
            logger.error(f"Hacker Newsからのデータ収集中にエラーが発生しました: {str(e)}")
            return []
    
    def _get_story_ids(self, url: str) -> List[int]:
        """
        ストーリーIDのリストを取得する
        
        Args:
            url: 取得先URL
            
        Returns:
            ストーリーIDのリスト
        """
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _get_item(self, item_id: int) -> Dict[str, Any]:
        """
        アイテムの詳細情報を取得する
        
        Args:
            item_id: アイテムID
            
        Returns:
            アイテムの詳細情報
        """
        url = f"{self.ITEM_URL}/{item_id}.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
