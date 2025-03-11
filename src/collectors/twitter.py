#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
X（Twitter）からのデータ収集モジュール
"""

import logging
import tweepy
from typing import List, Dict, Any
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TwitterCollector:
    """X（Twitter）からニュースを収集するクラス"""
    
    # AI関連のキーワードとハッシュタグ
    AI_KEYWORDS = [
        "artificial intelligence", "#AI", "#artificialintelligence", 
        "machine learning", "#ML", "#machinelearning",
        "deep learning", "#DL", "#deeplearning",
        "LLM", "大規模言語モデル", "#LLM", 
        "GPT", "ChatGPT", "#GPT", "#ChatGPT",
        "Anthropic", "Claude", "#Claude",
        "Gemini", "#Gemini",
        "AI開発", "AIモデル", "#AI開発"
    ]
    
    def __init__(
        self, 
        api_key: str, 
        api_secret: str, 
        access_token: str, 
        access_secret: str,
        max_tweets: int = 100
    ):
        """
        コンストラクタ
        
        Args:
            api_key: Twitter API キー
            api_secret: Twitter API シークレット
            access_token: アクセストークン
            access_secret: アクセスシークレット
            max_tweets: 取得する最大ツイート数
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.max_tweets = max_tweets
    
    def collect(self) -> List[Dict[str, Any]]:
        """
        X（Twitter）からニュースを収集する
        
        Returns:
            収集したニュースのリスト
        """
        logger.info("X (Twitter)からニュースの収集を開始")
        
        # API認証情報の確認
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            logger.error("Twitter API認証情報が不足しています")
            return []
        
        try:
            # Tweepy認証とAPIクライアントの初期化
            auth = tweepy.OAuth1UserHandler(
                self.api_key, self.api_secret,
                self.access_token, self.access_secret
            )
            api = tweepy.API(auth)
            
            # Twitter APIの動作確認
            api.verify_credentials()
            logger.info("Twitter APIの認証に成功しました")
            
            # 複数のキーワードでツイートを収集
            all_tweets = []
            for keyword in self.AI_KEYWORDS:
                try:
                    logger.info(f"キーワード '{keyword}' に関するツイートを検索しています")
                    
                    # 検索パラメータ設定
                    # 最大100件、7日以内、URLを含むもの、リツイートを除外
                    search_params = {
                        'q': f'{keyword} filter:links -filter:retweets',
                        'count': min(100, self.max_tweets),
                        'result_type': 'mixed',  # 人気と最新の混合
                        'tweet_mode': 'extended',  # フルテキスト取得
                        'lang': 'en'  # 英語ツイート
                    }
                    
                    tweets = api.search_tweets(**search_params)
                    
                    for tweet in tweets:
                        # 既に収集したツイートは重複させない
                        if tweet.id not in [t.get('twitter_id') for t in all_tweets]:
                            # URLを抽出
                            urls = []
                            if hasattr(tweet, 'entities') and 'urls' in tweet.entities:
                                for url_entity in tweet.entities['urls']:
                                    if 'expanded_url' in url_entity:
                                        urls.append(url_entity['expanded_url'])
                            
                            # ツイート情報を辞書形式で保存
                            tweet_info = {
                                'title': self._get_title_from_tweet(tweet),
                                'url': urls[0] if urls else f"https://twitter.com/i/web/status/{tweet.id}",
                                'content': tweet.full_text if hasattr(tweet, 'full_text') else tweet.text,
                                'source': 'Twitter',
                                'score': tweet.favorite_count,
                                'timestamp': int(tweet.created_at.timestamp()),
                                'comments_count': tweet.retweet_count,
                                'twitter_id': tweet.id,
                                'username': tweet.user.screen_name,
                                'urls': urls
                            }
                            
                            all_tweets.append(tweet_info)
                    
                    logger.info(f"キーワード '{keyword}' のツイートを{len(tweets)}件取得しました")
                    
                    # API制限を避けるため少し待機
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"キーワード '{keyword}' のツイート取得中にエラーが発生しました: {str(e)}")
            
            # 重複を削除
            unique_tweets = []
            seen_urls = set()
            
            for tweet in all_tweets:
                url = tweet['url']
                if url not in seen_urls:
                    seen_urls.add(url)
                    unique_tweets.append(tweet)
            
            logger.info(f"X (Twitter)から{len(unique_tweets)}件の一意なツイートを収集しました")
            return unique_tweets
            
        except Exception as e:
            logger.error(f"X (Twitter)からのデータ収集中にエラーが発生しました: {str(e)}")
            return []
    
    def _get_title_from_tweet(self, tweet) -> str:
        """
        ツイートからタイトルを抽出する
        
        Args:
            tweet: ツイートオブジェクト
            
        Returns:
            タイトル文字列
        """
        # フルテキストが利用可能ならそれを使用
        text = tweet.full_text if hasattr(tweet, 'full_text') else tweet.text
        
        # URLやメンションを削除
        if hasattr(tweet, 'entities'):
            # URLを削除
            if 'urls' in tweet.entities:
                for url in tweet.entities['urls']:
                    text = text.replace(url['url'], '')
            
            # メンションを削除
            if 'user_mentions' in tweet.entities:
                for mention in tweet.entities['user_mentions']:
                    text = text.replace(f"@{mention['screen_name']}", '')
        
        # 空白文字を整理
        text = ' '.join(text.split())
        
        # 長すぎる場合は切り詰める
        max_title_length = 100
        if len(text) > max_title_length:
            text = text[:max_title_length] + '...'
        
        return text
