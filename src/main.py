#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI News Aggregator
Product Hunt、Hacker News、X（Twitter）からAI関連ニュースを収集し日本語で要約するプログラム
"""

import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from collectors.hacker_news import HackerNewsCollector
from collectors.product_hunt import ProductHuntCollector
from collectors.twitter import TwitterCollector
from processors.ai_filter import AIContentFilter
from processors.summarizer import Summarizer
from utils.output_manager import OutputManager

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/ai_news_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """メイン処理"""
    # 環境変数のロード
    load_dotenv()
    
    try:
        # 各データソースからの収集
        logger.info("ニュースの収集を開始します")
        
        # Hacker Newsからの収集
        hn_collector = HackerNewsCollector()
        hn_news = hn_collector.collect()
        logger.info(f"Hacker Newsから{len(hn_news)}件のニュースを収集しました")
        
        # Product Huntからの収集
        ph_collector = ProductHuntCollector(api_key=os.getenv("PRODUCT_HUNT_API_KEY"))
        ph_news = ph_collector.collect()
        logger.info(f"Product Huntから{len(ph_news)}件のニュースを収集しました")
        
        # Twitterからの収集
        twitter_collector = TwitterCollector(
            api_key=os.getenv("TWITTER_API_KEY"),
            api_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        twitter_news = twitter_collector.collect()
        logger.info(f"X (Twitter)から{len(twitter_news)}件のニュースを収集しました")
        
        # 全ニュースの結合
        all_news = hn_news + ph_news + twitter_news
        logger.info(f"合計{len(all_news)}件のニュースを収集しました")
        
        # AI関連コンテンツのフィルタリング
        ai_filter = AIContentFilter()
        ai_news = ai_filter.filter(all_news)
        logger.info(f"AI関連ニュースとして{len(ai_news)}件をフィルタリングしました")
        
        # 日本語要約の生成
        summarizer = Summarizer(api_key=os.getenv("OPENAI_API_KEY"))
        summarized_news = summarizer.summarize(ai_news)
        logger.info(f"{len(summarized_news)}件のニュースを日本語に要約しました")
        
        # 結果の出力
        output_manager = OutputManager()
        output_path = output_manager.save(summarized_news)
        logger.info(f"要約結果を{output_path}に保存しました")
        
        return True
        
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    # ログディレクトリの作成
    os.makedirs("logs", exist_ok=True)
    
    # メイン処理の実行
    result = main()
    
    if result:
        logger.info("処理が正常に完了しました")
    else:
        logger.error("処理が異常終了しました")
