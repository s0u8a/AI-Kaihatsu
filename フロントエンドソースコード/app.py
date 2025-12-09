from flask import Flask, render_template, request, jsonify
import feedparser
import os
from dotenv import load_dotenv
import google.generativeai as genai

# =========================================
# .env 読み込み
# =========================================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
print("API KEY LOADED:", API_KEY)

# =========================================
# Gemini API 設定
# =========================================
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# =========================================
# Flask
# =========================================
app = Flask(__name__)

# =========================================
# 利用する RSS リスト
# =========================================
RSS_URLS = {
    "it": "https://news.yahoo.co.jp/rss/topics/it.xml",          # IT
    "sports": "https://news.yahoo.co.jp/rss/topics/sports.xml",  # スポーツ
    "economy": "https://news.yahoo.co.jp/rss/topics/business.xml"  # 経済
}


# =========================================
# タグ生成
# =========================================
def generate_tag(title, summary):
    try:
        prompt = f"""
        以下のニュース内容を1〜3語の日本語タグにしてください。
        出力はタグの文字列だけにしてください。

        タイトル: {title}
        要約: {summary}
        """

        response = model.generate_content(prompt)

        # デバッグ出力
        print("=== RESPONSE DEBUG ===")
        print(f"Title: {title}")
        print(f"Response type: {type(response)}")
        
        # レスポンス全体を確認
        try:
            response_dict = response.to_dict()
            print("Response dict:", response_dict)
        except Exception as e:
            print(f"to_dict() failed: {e}")
            print(f"Response object: {response}")
        
        print("======================")

        # レスポンス抽出（複数パターン対応）
        try:
            # パターン1: response.text
            if hasattr(response, "text") and response.text:
                tag = response.text.strip()
                print(f"✓ Got tag from response.text: {tag}")
                return tag
        except Exception as e:
            print(f"✗ response.text failed: {e}")

        try:
            # パターン2: response.candidates
            if hasattr(response, "candidates") and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # 安全性フィルターチェック
                if hasattr(candidate, "finish_reason"):
                    print(f"Finish reason: {candidate.finish_reason}")
                
                if hasattr(candidate, "safety_ratings"):
                    print(f"Safety ratings: {candidate.safety_ratings}")
                
                # content.parts からテキスト抽出
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            tag = part.text.strip()
                            print(f"✓ Got tag from parts: {tag}")
                            return tag
        except Exception as e:
            print(f"✗ candidates parsing failed: {e}")

        # どのパターンでも取得できなかった場合
        print("✗ No text found in response")
        return "タグ生成失敗"

    except Exception as e:
        print(f"!!! Gemini Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return "タグ生成エラー"


# =========================================
# HTML 画面
# =========================================
@app.route("/")
def index():
    return render_template("index.html")


# =========================================
# ニュース取得 API
# =========================================
@app.route("/news")
def get_news():
    category = request.args.get("category", "technology")
    rss_url = RSS_URLS.get(category)

    feed = feedparser.parse(rss_url)
    news_list = []

    for entry in feed.entries[:10]:  # 最低10件
        title = entry.title

        # Yahoo/NHK は summary が無い → title を使う
        summary = getattr(entry, "summary", "")
        if not summary or summary.strip() == "":
            summary = title

        link = entry.link

        tag = generate_tag(title, summary)

        news_list.append({
            "title": title,
            "summary": summary,
            "link": link,
            "tag": tag
        })

    return jsonify(news_list)


# =========================================
# 実行
# =========================================
if __name__ == "__main__":
    app.run(debug=True)
