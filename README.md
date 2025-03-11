# AI News Aggregator

Product Hunt、Hacker News、X（Twitter）からAIおよびAI開発に関連するニュースを収集し、日本語で要約するプログラムです。

## 機能

- 複数のソース（Product Hunt, Hacker News, X）からAI関連ニュースを収集
- AI関連コンテンツの抽出とフィルタリング
- 日本語での要約生成
- バッチ処理としての実行

## 使用方法

```bash
python main.py
```

## 必要な環境変数

- `OPENAI_API_KEY`: OpenAI APIキー
- `TWITTER_API_KEY`: Twitter APIキー
- `TWITTER_API_SECRET`: Twitter APIシークレット
- `TWITTER_ACCESS_TOKEN`: Twitter アクセストークン
- `TWITTER_ACCESS_SECRET`: Twitter アクセスシークレット
- `PRODUCT_HUNT_API_KEY`: Product Hunt APIキー
