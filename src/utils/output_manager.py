#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
出力管理モジュール
"""

import os
import json
import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class OutputManager:
    """ニュース要約結果を管理するクラス"""
    
    def __init__(self, output_dir: str = "output"):
        """
        コンストラクタ
        
        Args:
            output_dir: 出力ディレクトリ
        """
        self.output_dir = output_dir
        
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save(self, news_items: List[Dict[str, Any]]) -> str:
        """
        ニュース要約結果を保存する
        
        Args:
            news_items: 保存するニュースアイテムのリスト
            
        Returns:
            保存したファイルのパス
        """
        if not news_items:
            logger.warning("保存するニュースアイテムがありません")
            return ""
        
        # タイムスタンプ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 各形式で保存
        paths = {
            'json': self._save_json(news_items, timestamp),
            'csv': self._save_csv(news_items, timestamp),
            'txt': self._save_text(news_items, timestamp),
            'html': self._save_html(news_items, timestamp)
        }
        
        logger.info(f"ニュース要約結果を以下のファイルに保存しました: {', '.join(paths.values())}")
        
        # メインの出力はJSONとする
        return paths['json']
    
    def _save_json(self, news_items: List[Dict[str, Any]], timestamp: str) -> str:
        """
        JSON形式で保存
        
        Args:
            news_items: 保存するニュースアイテムのリスト
            timestamp: タイムスタンプ文字列
            
        Returns:
            保存したファイルのパス
        """
        output_path = os.path.join(self.output_dir, f"ai_news_{timestamp}.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(news_items, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def _save_csv(self, news_items: List[Dict[str, Any]], timestamp: str) -> str:
        """
        CSV形式で保存
        
        Args:
            news_items: 保存するニュースアイテムのリスト
            timestamp: タイムスタンプ文字列
            
        Returns:
            保存したファイルのパス
        """
        output_path = os.path.join(self.output_dir, f"ai_news_{timestamp}.csv")
        
        # DataFrameに変換して主要なカラムのみ保存
        df = pd.DataFrame(news_items)
        
        # 主要カラムの選択（存在する場合のみ）
        columns = [col for col in ['title', 'url', 'source', 'score', 'timestamp', 'summary_ja'] if col in df.columns]
        
        df[columns].to_csv(output_path, index=False, encoding='utf-8')
        
        return output_path
    
    def _save_text(self, news_items: List[Dict[str, Any]], timestamp: str) -> str:
        """
        テキスト形式で保存（人間可読なサマリー）
        
        Args:
            news_items: 保存するニュースアイテムのリスト
            timestamp: タイムスタンプ文字列
            
        Returns:
            保存したファイルのパス
        """
        output_path = os.path.join(self.output_dir, f"ai_news_{timestamp}.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"AI関連ニュース要約 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, item in enumerate(news_items, 1):
                f.write(f"[{idx}] {item.get('title', 'タイトルなし')}\n")
                f.write(f"ソース: {item.get('source', '不明')} (スコア: {item.get('score', 0)})\n")
                f.write(f"URL: {item.get('url', '不明')}\n")
                f.write("\n要約:\n")
                f.write(f"{item.get('summary_ja', '要約なし')}\n")
                f.write("\n" + "-" * 40 + "\n\n")
        
        return output_path
    
    def _save_html(self, news_items: List[Dict[str, Any]], timestamp: str) -> str:
        """
        HTML形式で保存（ブラウザで閲覧可能なレポート）
        
        Args:
            news_items: 保存するニュースアイテムのリスト
            timestamp: タイムスタンプ文字列
            
        Returns:
            保存したファイルのパス
        """
        output_path = os.path.join(self.output_dir, f"ai_news_{timestamp}.html")
        
        # HTMLの生成
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI関連ニュース要約 - {datetime.now().strftime('%Y-%m-%d')}</title>
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #333; }}
                .news-item {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
                .news-title {{ font-size: 1.4em; margin-top: 0; color: #0066cc; }}
                .news-meta {{ color: #666; font-size: 0.9em; }}
                .news-summary {{ line-height: 1.6; }}
                .news-url {{ word-break: break-all; }}
                .source-label {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; }}
                .source-hackernews {{ background-color: #ff6600; color: white; }}
                .source-producthunt {{ background-color: #da552f; color: white; }}
                .source-twitter {{ background-color: #1da1f2; color: white; }}
            </style>
        </head>
        <body>
            <h1>AI関連ニュース要約</h1>
            <p>生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="news-container">
        """
        
        # ニュースアイテムごとにHTMLを生成
        for item in news_items:
            source = item.get('source', '不明')
            source_class = source.lower().replace(' ', '')
            
            # 日時のフォーマット
            if 'timestamp' in item and item['timestamp']:
                date_str = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M')
            else:
                date_str = '日時不明'
            
            html_content += f"""
                <div class="news-item">
                    <h2 class="news-title">{item.get('title', 'タイトルなし')}</h2>
                    <div class="news-meta">
                        <span class="source-label source-{source_class}">{source}</span>
                        <span class="news-date">{date_str}</span>
                        <span class="news-score">スコア: {item.get('score', 0)}</span>
                    </div>
                    <div class="news-summary">
                        <p>{item.get('summary_ja', '要約なし')}</p>
                    </div>
                    <div class="news-url">
                        <a href="{item.get('url', '#')}" target="_blank">元記事を読む</a>
                    </div>
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
