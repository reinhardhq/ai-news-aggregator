#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Product Huntからのデータ収集モジュール
"""

import logging
import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProductHuntCollector:
    """Product Huntからニュースを収集するクラス"""
    
    API_URL = "https://api.producthunt.com/v1"
    POSTS_ENDPOINT = f"{API_URL}/posts"
    
    def __init__(self, api_key: str, days_back: int = 7):
        """
        コンストラクタ
        
        Args:
            api_key: Product Hunt API キー
            days_back: 何日前までのデータを取得するか
        """
        self.api_key = api_key
        self.days_back = days_back
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        Product Huntからニュースを収集する
        
        Returns:
            収集したニュースのリスト
        """
        logger.info("Product Huntからニュースの収集を開始")
        
        if not self.api_key:
            logger.error("Product Hunt APIキーが設定されていません")
            return []
        
        try:
            posts = []
            # 指定した日数分のデータを取得
            for day_offset in range(self.days_back):
                date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
                logger.info(f"{date}の製品を取得しています")
                
                day_posts = self._get_posts_for_day(date)
                posts.extend(day_posts)
                
                logger.info(f"{date}の製品を{len(day_posts)}件取得しました")
            
            # 収集したデータを整形
            news_items = []
            for post in posts:
                news_items.append({
                    'title': post.get('name', ''),
                    'url': post.get('discussion_url', ''),
                    'content': post.get('tagline', ''),
                    'source': 'Product Hunt',
                    'score': post.get('votes_count', 0),
                    'timestamp': int(datetime.strptime(post.get('created_at', ''), '%Y-%m-%dT%H:%M:%S.%fZ').timestamp()),
                    'comments_count': post.get('comments_count', 0),
                    'ph_id': post.get('id')
                })
            
            logger.info(f"Product Huntから{len(news_items)}件のニュースを収集しました")
            return news_items
            
        except Exception as e:
            logger.error(f"Product Huntからのデータ収集中にエラーが発生しました: {str(e)}")
            return []
    
    def _get_posts_for_day(self, date: str) -> List[Dict[str, Any]]:
        """
        指定した日の製品リストを取得する
        
        Args:
            date: 取得する日付（YYYY-MM-DD形式）
            
        Returns:
            製品リスト
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Host': 'api.producthunt.com'
        }
        
        params = {
            'day': date,
            'per_page': 50  # 1日あたりの最大取得数
        }
        
        response = requests.get(
            self.POSTS_ENDPOINT,
            headers=headers,
            params=params,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        return data.get('posts', [])
