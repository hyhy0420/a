from flask import Flask, redirect, abort
import random

app = Flask(__name__)

# アクセスカウントの設定
p = 2

# URLとアクセスカウントを管理するディクショナリ
urls = {
    "https://www.is.tohoku.ac.jp/media/files/ethics/03_170606re.pdf": p,
    "https://form.run/media/contents/googleform-message/": p,
    "https://shibboleth.nihon-u.ac.jp/idp/profile/SAML2/Redirect/SSO?execution=e1s1": p
}

@app.route('/')
def index():
    return render_template('distribute_url.html')  # HTML ファイルをレンダリング

def random_redirect():
    # アクセス可能なURLのリストを取得
    available_urls = [url for url, count in urls.items() if count > 0]

    if not available_urls:
        return "すべてのURLのアクセス回数が終了しました。", 403

    # ランダムにURLを選択
    chosen_url = random.choice(available_urls)
    
    # アクセスカウントを減らす
    urls[chosen_url] -= 1

    # 選択したURLにリダイレクト
    return redirect(chosen_url)

@app.route('/reset')
def reset_counts():
    # アクセスカウントをリセット
    for key in urls:
        urls[key] = p
    return "カウントがリセットされました。"

if __name__ == "__main__":
    app.run(debug=True)
