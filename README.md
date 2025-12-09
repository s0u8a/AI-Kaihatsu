# News App - Flask × Gemini API

このアプリは、Yahooニュース（IT / スポーツ / 経済）の RSS を取得し、  
Google Gemini API を使ってニュースごとにタグを自動生成して表示する Web アプリです。

---

# 📌 1. カテゴリ変更 → 画面表示までのロジック説明

## ■ 全体の流れ
1. ユーザーが画面上のカテゴリボタン（IT / スポーツ / 経済）をクリック  
2. フロントエンド（index.html / JavaScript）が `/news?category=xxx` にリクエスト  
3. Flask側（app.py）が該当 RSS URL を取得  
4. RSS からタイトル・概要・リンクを取得  
5. タイトルと概要を Gemini API に渡してタグを自動生成  
6. ニュースリスト＋タグを JSON でフロントへ返す  
7. HTML 側で記事カードとして描画される

---

## ■ 詳しい処理の流れ

### ① ユーザー操作（index.html）
フロント側でカテゴリボタンを押すと、JavaScript が以下のように API を呼び出します：

/news?category=it
/news?category=sports
/news?category=economy

yaml
コードをコピーする

---

### ② Flask がカテゴリに応じた RSS URL を選択
```python
RSS_URLS = {
    "it": "https://news.yahoo.co.jp/rss/topics/it.xml",
    "sports": "https://news.yahoo.co.jp/rss/topics/sports.xml",
    "economy": "https://news.yahoo.co.jp/rss/topics/business.xml"
}
③ RSS を feedparser で解析
python
コードをコピーする
feed = feedparser.parse(rss_url)
④ Gemini API でタグ生成
python
コードをコピーする
response = model.generate_content(prompt)
返ってきたテキストをタグとして使用します。

⑤ JSON でフロントに返却
python
コードをコピーする
return jsonify(news_list)
⑥ HTML に描画（JavaScript）
レスポンスを受け取った JS が、記事タイトル・概要・タグを HTML に反映します。

📌 2. Webサイトを動作させるために必要な環境構築・起動手順
⚙ 必要なもの
Python 3.10+

pip（Python パッケージ管理）

Git（任意）

Google Gemini API キー（.env に保存）

📦 インストール手順
① リポジトリをクローン（または ZIP 解凍）
bash
コードをコピーする
git clone https://github.com/あなたのユーザー名/news-app.git
cd news-app
② 必要ライブラリをインストール
css
コードをコピーする
pip install -r requirements.txt
③ .env を作成し API キーを記述
ini
コードをコピーする
GEMINI_API_KEY=あなたのAPIキー
📌 .env は GitHub へ公開しない（.gitignore で除外する）

▶ 起動
nginx
コードをコピーする
python app.py
ブラウザで以下を開く：

cpp
コードをコピーする
http://127.0.0.1:5000
📁 ファイル構成（例）
arduino
コードをコピーする
news-app/
│ app.py
│ .env  ← 公開禁止
│ requirements.txt
│ README.md
│
├─ templates/
│    └ index.html
│
└─ static/
     └ style.css


📌 使用技術
Python / Flask

feedparser

Google Gemini API

HTML / CSS / JavaScript

⚠ 注意点
APIキーは必ず .env に保存し、GitHub に載せない

無料枠には1日のリクエスト制限あり

タグ生成は API を大量に叩くため、制限に注意

