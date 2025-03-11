#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ニュース要約モジュール（日本語）
"""

import logging
import time
from typing import List, Dict, Any
import openai
import json

logger = logging.getLogger(__name__)

class Summarizer:
    """ニュースを日本語で要約するクラス"""
    
    # 要約指示プロンプト
    SUMMARY_PROMPT = """
    以下のAI技術に関するニュースを日本語で簡潔に要約してください。
    要約は200文字程度で、最も重要なポイントを含めてください。
    
    タイトル: {title}
    内容: {content}
    
    要約:
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        コンストラクタ
        
        Args:
            api_key: OpenAI API キー
            model: 使用するモデル名
        """
        self.api_key = api_key
        self.model = model
        
        # APIキーの設定
        openai.api_key = self.api_key
    
    def summarize(self, news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        ニュースアイテムを日本語で要約する
        
        Args:
            news_items: 要約するニュースのリスト
            
        Returns:
            要約を追加したニュースのリスト
        """
        logger.info(f"{len(news_items)}件のニュースを日本語で要約します")
        
        if not self.api_key:
            logger.error("OpenAI APIキーが設定されていません")
            return news_items
        
        summarized_items = []
        
        for idx, item in enumerate(news_items):
            try:
                logger.info(f"ニュース {idx+1}/{len(news_items)} を要約中...")
                
                # タイトルとコンテンツを取得
                title = item.get('title', '')
                content = item.get('content', '')
                
                # 要約用プロンプト作成
                prompt = self.SUMMARY_PROMPT.format(
                    title=title,
                    content=content
                )
                
                # OpenAI APIを使用して要約を生成
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "あなたはAI技術に関するニュースを簡潔に日本語で要約するアシスタントです。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.3,
                )
                
                # 要約結果を取得
                summary = response.choices[0].message.content.strip()
                
                # 要約をアイテムに追加
                item_with_summary = item.copy()
                item_with_summary['summary_ja'] = summary
                
                summarized_items.append(item_with_summary)
                
                # API制限を避けるため少し待機
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"ニュース {idx+1} の要約中にエラーが発生しました: {str(e)}")
                # エラーが発生しても元のアイテムは保存
                summarized_items.append(item)
        
        logger.info(f"{len(summarized_items)}件のニュースを日本語で要約しました")
        return summarized_items
