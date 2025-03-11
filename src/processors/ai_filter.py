#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI関連コンテンツのフィルタリングモジュール
"""

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class AIContentFilter:
    """AI関連コンテンツをフィルタリングするクラス"""
    
    # AI関連キーワードリスト
    AI_KEYWORDS = [
        # 一般的なAI用語
        'artificial intelligence', 'ai ', 'ai,', 'ai.', 'ai-', 'a.i.', 
        'machine learning', 'ml ', 'ml,', 'ml.', 'deep learning', 'dl ', 'dl,', 'dl.',
        'neural network', 'neural nets', 'algorithm', 'computer vision',
        
        # 特定のAIモデル・ツール
        'gpt', 'chatgpt', 'gpt-4', 'gpt-3', 'llm', 'large language model',
        'claude', 'gemini', 'midjourney', 'dalle', 'dall-e', 'stable diffusion',
        'openai', 'anthropic', 'meta ai', 'google bard', 'mistral', 'llama',
        
        # AI開発関連
        'prompt engineer', 'fine-tun', 'training', 'dataset',
        'transformer', 'diffusion model', 'gan ', 'gans', 'generative',
        'nlp', 'natural language processing', 'computer vision',
        'semantic', 'embedding', 'vector', 'tensor', 
        'language model', 'foundation model',
        
        # AI応用分野
        'ai agent', 'ai assistant', 'autonomous', 'automation',
        'recommendation system', 'personalization',
        'face recognition', 'speech recognition', 'voice assistant',
        
        # 特定の技術・手法
        'conv', 'transformers', 'attention mechanism', 'transfer learning',
        'reinforcement learning', 'self-supervised', 'unsupervised',
        'multimodal', 'semantic search', 'vector database',
        
        # 日本語キーワード
        '人工知能', 'ai', 'エーアイ', '機械学習', 'ディープラーニング',
        'ニューラルネットワーク', '大規模言語モデル', '生成ai', '生成モデル',
    ]
    
    def __init__(self, min_score: int = 5):
        """
        コンストラクタ
        
        Args:
            min_score: フィルタを通過するための最小スコア
        """
        self.min_score = min_score
        # キーワード検索用の正規表現パターンをコンパイル
        self.keyword_patterns = [
            re.compile(r'\b' + re.escape(keyword.lower()) + r'\b', re.IGNORECASE)
            for keyword in self.AI_KEYWORDS
        ]
    
    def filter(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        AI関連のニュースをフィルタリングする
        
        Args:
            news_items: フィルタリング対象のニュースリスト
            
        Returns:
            フィルタリング後のニュースリスト
        """
        logger.info(f"{len(news_items)}件のニュースをAI関連フィルタリングします")
        
        ai_related_news = []
        
        for item in news_items:
            # スコアの最低値チェック
            if item.get('score', 0) < self.min_score:
                continue
            
            # タイトルとコンテンツを結合してチェック
            combined_text = (
                f"{item.get('title', '')} {item.get('content', '')}"
            ).lower()
            
            # AI関連キーワードの出現をチェック
            is_ai_related = any(
                pattern.search(combined_text)
                for pattern in self.keyword_patterns
            )
            
            if is_ai_related:
                ai_related_news.append(item)
        
        logger.info(f"AI関連として{len(ai_related_news)}件のニュースを抽出しました")
        return ai_related_news
