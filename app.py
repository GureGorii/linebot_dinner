import time
import pandas as pd
import random

import requests
from bs4 import BeautifulSoup

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

#返信する型をインポート（文字、スタンプ、画像）
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

#料理名生成ボット
#デプロイ : https://dinnerlinebot.herokuapp.com/
#URL : https://lin.ee/13Qcozt
app = Flask(__name__)

line_bot_api = LineBotApi('##api_key##')
handler = WebhookHandler('##handler##')

@app.route("/")
def test():
    return "ハローワールド"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

users = {}
@handler.add(MessageEvent, message=TextMessage)
#料理生成関数
def handle_message(event):
    #関数定義
    def picture(word):
        load_url = f"https://www.google.com/search?q={word}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwir6rm56uryAhXXwosBHdxTBQIQ_AUoAnoECAIQBA&biw=1366&bih=657"
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")
        images = soup.find_all('img')
        del images[0]
        image_url = random.choice(images)['src']

        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )

    def picture_c(word):
        load_url = f"https://www.google.co.jp/search?q={word}&tbm=isch&chips=q:{word},g_1:かわいい:PN1wyKqcPdc%3D&hl=ja&sa=X&ved=2ahUKEwjF2dm4pezzAhVHy4sBHar0DrcQ4lYoAXoECAEQFA&biw=1587&bih=773"
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")
        images = soup.find_all('img')
        del images[0]
        image_url = random.choice(images)['src']

        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )

    #userId = event.source.user_id
    #料理名生成
    menu = ['サラダチキン','塩豚丼','酢豚','和風パスタ','肉じゃが','ぶりの照り焼き', '納豆ご飯', '水鍋', 'ミルフィーユ鍋', 'ラーメン', 'ステーキ', '親子丼', '玉子焼き', '鶏のから揚げ', '肉じゃが', '天ぷら', 'きんぴら', '鶏の照り焼き', '五目炊き込みごはん', '筍ごはん', 'おでん', 'すき焼き', '切り干し', 'ひじきの煮物', 'さばの味噌煮', '生姜焼き', '牛丼', '筑前煮', 'さといもの煮ころがし', 'ぬた和え', 'ふろふき', '肉豆腐', 'きゅうりとわかめの酢の物', 'かぼちゃの煮物', '卯の花', '三色丼', 'イカの刺身', 'ほうれん草のごまあえ', 'カレイの煮付け', '豚汁', '鶏の竜田揚げ', '鯵の南蛮漬け笹', 'はまぐりのお吸い物', '茶碗蒸し', 'まぐろの漬け丼', '鯵のたたき', '鯛の昆布じめ', 'ゴーヤチャンプルー', '栗ごはん', '秋刀魚の蒲焼', '蕎麦', '栗きんとん', '伊達巻', '黒豆艶煮', '鰯のつみれ汁', 'あら汁', '西京焼き', 'ちりめん山椒', '金目鯛の煮付け', '揚げ出し豆腐', '茄子の旨煮', '塩鮭の冷やし茶漬け', '青菜のおひたし', '胡麻豆腐', '', '鯖の幽庵焼', '鶏と冬瓜のにゅうめん', '田作り', '叩きごぼう', 'なます', '鯛骨蒸し', '牡蠣釜飯', '銀ダラの粕漬け', 'なすの田楽', 'なすの丸炊き', '鰆のごま茶漬け越智', 'がんもどき', '若筍汁', 'ポテトサラダ', '豆腐入りハンバーグ', '玉葱ステーキ', '胡麻酢和え', 'オムライス', 'エビフライ', 'ローストビーフ', 'コールスロー', 'ポテトサラダ', 'マカロニグラタン', 'ビーフポテトコロッケ', 'ロールキャベツ', 'ナポリタン', 'エビピラフ', 'ハンバーグステーキ', 'マカロニサラダ', 'カミカツ', 'ドライカレー', 'カニクリームコロッケ', 'クリームシチュー', 'コンソメスープ', 'メンチカツ', 'エッグベネディクト', 'ハンバーガー', 'スモークチキン', 'チリコンカーン', 'オムライス', 'フライドチキン', 'ミートローフ', 'ツヴィーベルクーヘン', 'マウルタッシェン', 'ユワレラキア', 'メリジャネス・イマン・バルディ', '魚介カタプラーナ', 'バカリャウ・ア・ブラーシュ', 'にんじんのポタージュ', 'エビチリ', '酢豚', 'あんかけ', 'サンラータン', 'にらたま', 'チャーハン', '青椒肉絲', '坦々麺', '紅油水餃～ホンユースイジャオ～', '棒々鶏', '冷やし中華', '肉だんご', 'あさりの中華粥', '春巻き', '卵スープ', '麻婆豆腐', '回鍋肉', '焼きそば', '白身魚の姿蒸し', 'イカのミルク炒め', '麻婆春雨', '麻婆茄子', '鶏肉とカシューナッツのピリ辛炒', '中華ちまき', '鶏肉のスパイシー炒め', '卵とトマトの炒めもの', '八宝菜', '茹でワンタン', '揚げワンタン', 'テリーヌ', 'ムニエル', 'ビーフシチュー', 'コーンポタージュ', 'ビーフストロガノフ', 'かぼちゃの冷製クリームスープ', 'ポトフー', 'ラタトゥイユ', 'マダイのカルパッチョ', 'レバーペースト', 'シーザーサラダ', 'ポークソテー', 'オニオングラタンスープ', 'ピサラディエール', 'パテ', 'ブイヤベース', 'キッシュ', '白身魚のポワレ', 'マッシュポテト', '鶏胸肉のポッシェ', '豚肉のリエット', '豚ばら肉のコンフィ', '鶏肉のコンフィ', 'チキンのトマト煮込み', 'ポタージュ', '鶏手羽のア・ラ・プロヴァンサル', 'チキン・コルドン・ブルー','グラタン', '豚フィレ肉のピカタ', 'チーズスフレ', '若鶏のバロティーヌ', '干鱈とじゃがいものブランダード', 'アーティチョークのバリグール', 'ペペロンチーノ', 'バーニャカウダ', 'トマトの冷製パスタ', 'カルボナーラ', 'いわしの香草焼き', 'アクアパッツァ', 'シチリア風カポナータ', 'ポモドーロ', 'ジェノベーゼ', 'モンタナーラ', 'ミラノ風カツレツ', '魚介のフリット・ミスト', 'グリッシーニ', 'ミネストローネ', '4種のチーズ入り', 'パルメジャーノチーズのリゾット', 'ステーキ', 'トマトソースのスパゲティ', 'ズッキーニのフリッタータ', 'インペパータ', 'ボンゴレ', 'ペンネ', '鶏もも肉のカチャトーラ片', 'ポルペットーネ', 'ピッツァ', 'スパゲッティ', 'オムレツ', '若鶏のトマト煮込み', '鶏肉のアヒージョ', '海老のアヒージョ', 'マッシュルームのアヒージョ', '魚介のパエリア', 'ナシゴレン', 'トッポギ呉本', 'ビビンパ', 'チャプチェ', '海鮮チヂミ', '鶏肉のグリーンカレー', '鶏挽き肉のバジル炒め', 'スウドゥブチゲ', 'ナムル', '春雨サラダ', 'キンパ', 'ヘムルチョンゴル', '参鶏湯（サムゲタン）', 'ラープガイ（鶏ひき肉のサラダ）', 'バターチキンカレー', '南インド風チキンカレー', 'ほうれん草のカレー', 'キーマカレー', 'フィッシュカレー', 'ポリヤル（キャベツのポリヤル）', 'サモサ', 'プラウンマサラ（海老カレー）', 'チャナマサラ', 'ホレシュテ', 'ククサブジ', 'ポークカレー', '杏仁豆腐', 'マドレーヌ', 'パンナコッタ', 'チョコチップクッキー', 'ティラミス', 'リンゴとバナナのケーキ', 'チョコレートケーキ', 'チョコレートムース', 'イチゴのレアチーズケーキ', 'マンゴープリン', 'ふわふわロールケーキ', 'アップルパイ', 'みたらし団子', 'わらび餅', 'ミルティーユ鍋', 'シュークリーム', 'イチゴのショートケーキ', 'プロフィットロール', 'ブリオッシュのフレンチトースト', 'ブリュッセル風ワッフル', 'カスタードプリン', 'タピオカココナッツミルク', 'パォン・デ・ロー', '草餅']
    if event.message.text == "ご飯" or event.message.text == "ごはん" or event.message.text == "今日のご飯" or event.message.text == "今日のごはん":
        reply_message = random.choice(menu)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    #金曜ロードショー
    elif event.message.text == "金曜ロードショー" or event.message.text == "金曜" or event.message.text == "金曜日":
        load_url = "https://kinro.ntv.co.jp/lineup"
        html = requests.get(load_url)
        soup = BeautifulSoup(html.content, "html.parser")

        # classの部分を入力し、表示したいタグを入力
        lineup = soup.find(class_="list")
        fryday = ""
        for element in lineup.find_all(class_="cap"):
            date = element.find(class_="date")
            title = element.find(class_="title")    
            fryday += "\n" + date.text + " " +title.text
        reply_message = f"金曜ロードショーのラインナップは{fryday}\n です。"
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    else :
        reply_message = f"「{event.message.text}」に応答する言葉はありません。"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

if __name__ == "__main__":
    app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
