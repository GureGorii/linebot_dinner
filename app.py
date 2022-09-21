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
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    TemplateSendMessage,ButtonsTemplate,URIAction,ImageSendMessage
)

from linebot.exceptions import LineBotApiError


#料理名生成ボット
#heroku : https://dinnerlinebot.herokuapp.com/
app = Flask(__name__)

line_bot_api = LineBotApi('K+PeCh2yWmBBpwQphFcYa5XdSzXU8pwn77zK4zsPvyFA6/gLukpoVyGRxn/gwIXLFACkPYWWdVUZHVwz8RgJg2YzcawVljXxx6qLokdcekqOuCNPT3jB9hBk6dK5DWPE0c3J0UqWPHAhKyw/uPhQ5AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('70963e756556122179c214c35f8571d8')

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
    
    wasyoku = ['肉じゃが','ぶりの照り焼き','とんかつ','からあげ','チキン南蛮','サバの味噌煮','さんまの塩焼き','だし巻き卵','親子丼','かつ丼','炊き込みご飯','きんぴらごぼう','味噌汁','うどん','そば','照り焼きチキン','天ぷら','生姜焼き','タコの酢の物','おひたし','筑前煮','すまし汁','おでん','すき焼き','納豆ご飯','刺身','海鮮丼','サラダチキン']
    yosyoku = ['オムライス','コロッケ','カレー','ハヤシライス','ハンバーグ','ハンバーガー','ビーフシチュー','チキンライス','グラタン','ロールキャベツ','パスタ','シチュー','サラダチキン','ローストチキン','ローストビーフ']
    tyuka = ['麻婆豆腐','麻婆茄子','エビチリ','餃子','チャーハン','ラーメン','酢豚','八宝菜','回鍋肉','春巻き','肉まん','シュウマイ']

    comment = ['天気がいいので','天気が悪いので','少し肌寒いので','暖かいので','外で食べたい気分なので','チートデイなので','昨日はご飯だったので','あまりお腹がすいていないので','サラダチキンの気分なので']

    if event.message.text == "今日のご飯" or event.message.text == "今日のごはん":
        #reply_message = "今日のご飯はサラダチキンはどうですか？"
        #df = pd.read_csv('menu.csv')
        #print(df)
        reply_message = random.choice(menu)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        
    #ボタンテンプレート(製作中)
    elif event.message.text == "ご飯" or event.message.text == "ごはん":
        messages= TemplateSendMessage(
            alt_text="ごはん",
            template=ButtonsTemplate(
                text="何が食べたい気分ですか？",
                title="料理を提案します",
                image_size="cover",
                thumbnail_image_url="https://www.shimay.uno/nekoguruma/wp-content/uploads/sites/2/2018/03/20171124_194201-508x339.jpg",
                imageBackgroundColor="#FFFFFF",
                actions=[
                    {
                        "type": "message",
                        "label": "和食",
                        "text": "和食"
                    },
                    {
                        "type": "message",
                        "label": "洋食",
                        "text": "洋食"
                    },
                    {
                        "type": "message",
                        "label": "中華",
                        "text": "中華"
                    },
                    {
                        "type": "message",
                        "label": "その他",
                        "text": "その他"
                    }
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            messages=messages
        )
    
    elif event.message.text == "和食":
        reply_message = "今日は" + random.choice(comment) + random.choice(wasyoku) + "はいかがですか？"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    elif event.message.text == "洋食":
        reply_message = "今日は" + random.choice(comment) + random.choice(yosyoku) + "はいかがですか？"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    elif event.message.text == "中華":
        reply_message = random.choice(tyuka)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    
    elif event.message.text == "その他":
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
            #print(date.text)
            #print(title.text)
            fryday += "\n" + date.text + " " +title.text
        reply_message = f"金曜ロードショーのラインナップは{fryday}\n です。"
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        
        
        

    #有名人の画像送信
    elif event.message.text == "有村架純" or event.message.text == "ありむらかすみ" or event.message.text == "あ":
        picture_c("有村架純")
    elif event.message.text == "齋藤飛鳥" or event.message.text == "さいとうあすか" or event.message.text == "さ":
        picture_c("齋藤飛鳥")
    elif event.message.text == "中村倫也" or event.message.text == "なかむらともや" or event.message.text == "な":
        picture("中村倫也")
    elif event.message.text == "浜辺美波" or event.message.text == "はまべみなみ" or event.message.text == "は":
        picture_c("浜辺美波") 
    elif event.message.text == "福原遥" or event.message.text == "ふくはらはるか" or event.message.text == "ふ":
        picture("ふくはらはるか")
    elif event.message.text == "インド" or event.message.text == "インド人" or event.message.text == "笑顔":
        picture("インド人+笑顔")

    # エラー
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