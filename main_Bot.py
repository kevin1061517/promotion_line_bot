#fang_test herokuapp
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    SourceUser,SourceGroup,SourceRoom,LeaveEvent,JoinEvent,
    TemplateSendMessage,PostbackEvent,AudioMessage,LocationMessage,
    ButtonsTemplate,LocationSendMessage,AudioSendMessage,ButtonsTemplate,
    ImageMessage,URITemplateAction,MessageTemplateAction,ConfirmTemplate,
    PostbackTemplateAction,ImageSendMessage,MessageEvent, TextMessage, 
    TextSendMessage,StickerMessage, StickerSendMessage,DatetimePickerTemplateAction,
    CarouselColumn,CarouselTemplate,VideoSendMessage,ImagemapSendMessage,BaseSize,
    URIImagemapAction,MessageImagemapAction,ImagemapArea,ImageCarouselColumn,ImageCarouselTemplate,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,URIAction,LocationAction,QuickReply,QuickReplyButton,
    DatetimePickerAction,PostbackAction,MessageAction,CameraAction,CameraRollAction
)
#from imgurpython import ImgurClient
import os
import random
from bs4 import BeautifulSoup as bf
import requests
from datetime import timedelta, datetime
#import json
from firebase import firebase
from web_crawler import *
app = Flask(__name__)
url = os.getenv('firebase_bot',None)
fb = firebase.FirebaseApplication(url,None)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET', None))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body,signature)
    except LineBotApiError as e:
        print("Catch exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("ERROR is %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)
    print('---------ok-----------')
    return 'OK'

def movie_template():
    buttons_template = TemplateSendMessage(
    alt_text='電影 template',
    template=ButtonsTemplate(
            title='KaKa電影院',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/zzv2aSR.jpg',
            actions=[
                    MessageTemplateAction(
                        label='Yahoo本週新片',
                        text='yahoo_movie'
                    ),
                    MessageTemplateAction(
                       label='開天眼電影介紹',
                        text='開天眼電影介紹'
                    ),
                    MessageTemplateAction(
                        label='觸電網頻道',
                        text='觸電網-youtube'
                    )
                ]
            )
    )
    return buttons_template

def template_stage():
    buttons_template = TemplateSendMessage(
        alt_text='stage template',
        template=ButtonsTemplate(
            title='STAGE',
            text='KaKa的各個Stage',
            thumbnail_image_url='https://i.imgur.com/WoPQJjB.jpg',
            actions=[
                MessageTemplateAction(
                        label='大學',
                        text='大學'
                ),
                MessageTemplateAction(
                        label='研究所',
                        text='研究所'
                ),
                MessageTemplateAction(
                        label='出社會',
                        text='出社會'
                )
            ]
         )
    )
    return buttons_template


#判斷是西洋還是華語歌曲 如果為西洋category是390 而華語是297
def type_music(category,range_num=5):
    template = []
    yesterday = datetime.today() + timedelta(-1)
    yesterday_format = yesterday.strftime('%Y-%m-%d')
    t = 'https://kma.kkbox.com/charts/api/v1/daily?category='+str(category)+'&date='+yesterday_format+'&lang=tc&limit=50&terr=tw&type=song'
    res = requests.get(t).json()
    for i in range(range_num-5,range_num):
        template.append(process_mp3_template(res['data']['charts']['song'][i]['song_name'],i+1,res['data']['charts']['song'][i]['cover_image']['normal'],res['data']['charts']['song'][i]['artist_name'],res['data']['charts']['song'][i]['song_url'],process_mp3_url('https://www.kkbox.com/tw/tc/ajax/wp_songinfo.php?type=song&crypt_id='+res['data']['charts']['song'][i]['song_id']+'&ver=2'),range_num,category))
    return template


#一個模板來放抓來的音樂並顯示連結
def process_mp3_template(title,rank,album_image,singer,song_url,listen_url,range_num,category):
    if song_url == '#':
        label = '無介紹與歌詞'
        song_url = 'https://github.com/kevin1061517?tab=repositories'
    else:
        label = '介紹及歌詞'
    buttons_template = TemplateSendMessage(
        alt_text='mp3_template',
        template=ButtonsTemplate(
            title = '排行榜第{}名'.format(rank),
            text='歌手:{}\n歌名:{}'.format(singer,title)[:60],
            thumbnail_image_url = album_image,
            actions=[
                URITemplateAction(
                    label = label,
                    uri = song_url
                ),
                PostbackTemplateAction(
                    label='試聽30秒',
                    data = 'listen'+listen_url,
                    text = '請稍等一下，載入資料'
                ),
                PostbackTemplateAction(
                    label = '再看看{}名~{}名 歌曲'.format(range_num+1,range_num+5),
                    data = 'next'+str(range_num+5)+str(category),
                    text = '請稍等一下，載入資料'
                )
            ]
         )
    )
    return buttons_template


@handler.add(PostbackEvent)
def handle_postback(event):
    temp = event.postback.data
    if temp[3:] == 'contest':
        url = 'https://i.imgur.com/d3zQFeB.jpg'
        line_bot_api.reply_message(event.reply_token,[
                TextSendMessage(text='上個月參加朝陽科技大學舉辦的資訊科技創意大賽，以題目為LINE  BOT實作問卷系統拿到佳作'),
                ImageSendMessage(
                        original_content_url=url,
                        preview_image_url=url
                        )])
    elif temp[3:] == 'experience':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='這學期在國泰世華銀行擔任CSP資訊實習生，學習銀行資訊系統開發與軟體測試，過程中我用C#開發小工具協助部門作業效率，給我一個很棒的機會去學習'))
    elif temp[3:] == 'run':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='目前已經參加了5次的馬拉松，於前年開始迷上，目前都是參加半碼21K的賽事，期待未來能完成更多自己的里程碑'))
    elif temp[3:] == 'blog':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='很開心日前部落格來訪人數破了1萬，目前都是寫一些學習心得以及遇到的問題並解決的過程，喜歡分享學到的東西在網路上面，尤其是資訊程式方面的文章，會持續在部落格上做出貢獻，希望能藉由一己之力，幫助其他遇到相同問題的同伴們!!\n我的部落格: http://b0212066.pixnet.net/blog'))
    elif temp[3:] == 'eng':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='KaKa的英文都有持續再努力，前幾個月多益考800分，對於英文抱著不中斷不放棄!!!因為在看LINE developer文件時候都是需要用到英文'))
    elif temp[:6] == 'listen':
        url = temp[6:]
        if url == '音樂版權未授權~':
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='音樂版權未授權~'))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                AudioSendMessage(original_content_url=url,duration=30000)
            )
    elif temp[:4] == 'next':
        range_num = int(temp[4:-3])
        if range_num > 50:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已經到底了喔!!'))
        else:
            category = int(temp[-3:])
            template = type_music(category,range_num)    
            line_bot_api.reply_message(event.reply_token,template)
    elif temp[:4] == 'else':
        t = template_stage()
        line_bot_api.reply_message(event.reply_token,t)
    elif temp == 'word':
        profile = line_bot_api.get_profile(event.source.user_id)
        name = profile.display_name
        call = os.getenv('call',None)
        template = TemplateSendMessage(
            alt_text='buttons_template',
            template=ButtonsTemplate(
                title = '{}前輩!想給我什麼話'.format(name),
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/48ezKDC.jpg',
                actions=[
                    PostbackTemplateAction(
                        label='給KaKa的話',
                        data = 'talk'
                        ),
                    URITemplateAction(
                        label='連絡我好消息~',
                        uri='tel://{}'.format(call)
                        )
                ]))
        line_bot_api.reply_message(event.reply_token,template)
    elif temp == 'talk':
        fb.post('/talk','Y')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='接下來請打要跟KaKa說的話👇👇👇'))

# 處理訊息:
@handler.add(MessageEvent, message=TextMessage)
def handle_msg_text(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    name = profile.display_name
    t = fb.get('/talk',None)
    flag = ''
    if t:
        flag = list(t.values())[0]
    if flag == 'Y':
        kaka_id = os.getenv('user_id',None)
        fb.delete('/talk',None)
        line_bot_api.push_message(kaka_id, TextSendMessage(text='{}前輩給我的話:\n{}'.format(name,event.message.text)))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='成功傳給KaKa'))   
    if event.message.text.lower() == 'test':
        t =event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=t)
        )
    if event.message.text.lower() == 'hi':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='hello world~')
        )
    elif event.message.text.lower() == 'hobby':
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='My hobby', weight='bold', size='xl',color='#006400'),
                    # review
                    TextComponent(
                            text='kaka平常的休閒興趣，彙總起來做查詢!',
                            size='sm',wrap=True,color='#2E8B57'
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    ImageComponent(
                                        url='https://i.imgur.com/dTlQ9gK.png',
                                        size='full',
                                        flex=2,
                                        aspect_ratio='2:2',
                                        aspect_mode='cover'
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color='#99FF99',
                                        gravity = 'center',
                                        flex=8,
                                        action=MessageAction(label='Movies', text='Movies')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                   ImageComponent(
                                        url='https://i.imgur.com/Mce9Krj.png',
                                        size='full',
                                        flex=2,
                                        aspect_ratio='2:2',
                                        aspect_mode='cover'
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color='#99FF99',
                                        gravity = 'center',
                                        flex=8,
                                        action=MessageAction(label='Music', text='Music')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                   ImageComponent(
                                        url='https://i.imgur.com/SWotQON.png',
                                        size='full',
                                        flex=2,
                                        aspect_ratio='2:2',
                                        aspect_mode='cover'
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        gravity = 'center',
                                        color='#99FF99',
                                        flex=8,
                                        action=MessageAction(label='Marathon', text='Marathon')
                                        )
                                ],
                            )
                        ],

                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=MessageAction(label='My Record', text='record')
                    )
                ]
            )
        )   
        message = FlexSendMessage(alt_text="hobby", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#menu用來指引所有流程動線
    elif event.message.text.lower() == 'menu':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/TPELVeP.jpg',
                size='full',
                aspect_ratio='5:3',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                spacing = 'xs',
                contents=[
                        
                    # title
                    TextComponent(text='幫你帶路一下', weight='bold', size='lg'),
                    # review
                    TextComponent(
                            text='由於寫的流程函式有點多，所以把所有的功能列在此，希望能讓{}前輩更了解KaKa'.format(name),
                            size='xs',wrap=True
                    ),
                    TextComponent(
                            text='by熱愛Coding的boy'.format(name),
                            size='xs',wrap=True,align='end'
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=MessageAction(label='KaKa的歷程', text='kaka')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=MessageAction(label='KaKa的興趣', text='hobby')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=MessageAction(label='KaKa的紀錄', text='record')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=MessageAction(label='KaKa的真話', text='出社會')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=URIAction(label='KaKa的 BLOG', uri='line://app/1567668860-0Q8dm5AB')
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='🔜',
                                        size='xl',
                                        flex = 2
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        color ='#99FF99',
                                        flex=10,
                                        action=PostbackAction(label='給KaKa的話', data='word')
                                    )
                                ],
                            )
                        ],

                    ),
                ],
            )
        )   
        message = FlexSendMessage(alt_text="undergraduate", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    elif event.message.text.lower() == 'kaka':
        _id = os.getenv('second_richmenu',None)
        headers = {"Authorization":"Bearer {}".format(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None)),"Content-Type":"application/json"}
        req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(_id),headers=headers)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, _id)
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text='{} 前輩您好!\n請查看一下Rich menus有所變化，希望能讓您更了解KaKa'.format(name)),
             TextSendMessage(text='下面喔👇👇👇👇')]
        )
    elif event.message.text.lower() == 'movies':
        template = movie_template()
        line_bot_api.reply_message(
            event.reply_token,
            template
        )
    elif event.message.text.lower() == 'yahoo_movie':
        title,img = yahoo_movie()
        t = [ImageComponent(
                url=i,
                size='full',
                flex=3,
                gravity = 'center',
                aspect_ratio='5:3',
                aspect_mode='cover'
                ) for i in img]
        t1 = [TextComponent(
                text=i,
                wrap=True,
                size='sm',
                ) for i in title]

        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/zzv2aSR.jpg',
                size='full',
                aspect_ratio='11:7',
                aspect_mode='cover',
                action=URIAction(uri='https://movies.yahoo.com.tw/movie_thisweek.html?guccounter=1&guce_referrer=aHR0cHM6Ly9tb3ZpZXMueWFob28uY29tLnR3Lw&guce_referrer_sig=AQAAAIeddc72iLVwqIgS4Gb-SjqupoXFeFl-3ffJ90Y83F-fqYQiUCtA4lOFtWirZQqWexqJTDaRQMajC35ss4y3RG90c3C0vi-EtazGMtt0k3pO6wboGgESRnNu0pVU59bPlKIRRzUHsn4joqFtHDeLdIs8o1GyYluxgQ_bCkSMBrnv', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Yahoo本週電影', weight='bold', size='xl'),
                    # review
                    TextComponent(
                            text='網路爬蟲的實作~',
                            size='sm',wrap=True
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    BoxComponent(
                                        layout='vertical',
                                        spacing='sm',
                                        flex=3,
                                        contents=t
                                    ),
                                    BoxComponent(
                                        layout='vertical',
                                        spacing='sm',
                                        flex=7,
                                        contents=t1
                                    )
                                ],
                            )
                        ],

                    ),
                ],
            ),
        )   
        message = FlexSendMessage(alt_text="hobby", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.message.text == "開天眼電影介紹":
        content = movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content),
        )
    elif event.message.text.lower() == "觸電網-youtube":
        target_url = 'https://www.youtube.com/user/truemovie1/videos'
        rs = requests.session()
        res = rs.get(target_url, verify=False)
        soup = bf(res.text, 'html.parser')
        seqs = ['https://www.youtube.com{}'.format(data.find('a')['href']) for data in soup.select('.yt-lockup-title')]
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
            ])
    elif event.message.text.lower() == "music":
        buttons_template = TemplateSendMessage(
            alt_text='kkbox template',
            template=ButtonsTemplate(
                title='kkbox歌曲熱門排行',
                text='請選擇需要選項',
                thumbnail_image_url='https://i.imgur.com/WWJ1ltx.jpg',
                actions=[
                    MessageTemplateAction(
                        label='華語',
                        text='kkbox-華語'
                    ),
                    MessageTemplateAction(
                        label='西洋',
                        text='kkbox-西洋'
                    ),
                    MessageTemplateAction(
                        label='日語',
                        text='kkbox-日語'
                    ),
                    MessageTemplateAction(
                        label='台語',
                        text='kkbox-台語'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        #https://kma.kkbox.com/charts/api/v1/daily?category=297&date=2018-12-17&lang=tc&limit=50&terr=tw&type=song
    elif event.message.text == "kkbox-華語":
        template = type_music(297)
        line_bot_api.reply_message(event.reply_token,template)
#https://kma.kkbox.com/charts/api/v1/daily?category=390&date=2018-12-17&lang=tc&limit=50&terr=tw&type=song
    elif event.message.text == "kkbox-西洋":
        template = type_music(390)
        line_bot_api.reply_message(event.reply_token,template)
    elif event.message.text == "kkbox-日語":
        template = type_music(308)
        line_bot_api.reply_message(event.reply_token,template)
    elif event.message.text == "kkbox-台語":
        template = type_music(304)
        line_bot_api.reply_message(event.reply_token,template)
    elif event.message.text == 'Marathon':
        item = run()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=item))
    elif event.message.text == 'record':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='想看我哪些紀錄呢，就講今年的而已喔!',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(label="比賽", data="qc_contest")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="經驗", data="qc_experience")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="馬拉松", data="qc_run")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="部落格", data="qc_blog")
                        ),
                        QuickReplyButton(
                            action=PostbackAction(label="英文能力", data="qc_eng")
                        )
                    ])))
#查看rich_menu
    elif event.message.text.lower() == 'all_richmenu':
        t= ''
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print(rich_menu.rich_menu_id)
            t += rich_menu.rich_menu_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=t)
        )
#建立rich_menu
#    elif event.message.text.lower() == 'test2': 
#        line_bot_api.delete_rich_menu('richmenu-03192095e33c6866fefd0c486cc054ce')
##        line_bot_api.delete_rich_menu('richmenu-03192095e33c6866fefd0c486cc054ce')
#        headers = {"Authorization":"Bearer {}".format(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None)),"Content-Type":"application/json"}
#        body = {
#                "size": {"width": 2500, "height": 843},
#                "selected": "true",
#                "name": "Controller",
#                "chatBarText": "Controller",
#                "areas":[
#                        {
#                            "bounds": {"x":0, "y": 496, "width": 720, "height": 345},
#                            "action": {"type": "message", "text": "回主畫面"}
#                        },
#                        {
#                            "bounds": {"x": 720, "y": 400, "width": 590, "height": 440},
#                            "action": {"type": "message", "text": "大學"}
#                        },
#                        {
#                            "bounds": {"x": 1310, "y": 400, "width": 600, "height": 440},
#                            "action": {"type": "message", "text": "研究所"}
#                        },
#                        {
#                            "bounds": {"x": 1910, "y": 400, "width": 595, "height":440},
#                            "action": {"type": "message", "text": "出社會"}
#                        }
#                ]
#            }
#        req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', headers=headers,data=json.dumps(body).encode('utf-8'))
#        print(req.text)
#        line_bot_api.reply_message(
#            event.reply_token,
#            TextSendMessage(text=req.text)
#        )
#    elif event.message.text.lower() == 'test3':
#        
#        headers = {"Authorization":"Bearer {}".format(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None)),"Content-Type":"application/json"}
#        rich_menu_list = line_bot_api.get_rich_menu_list()
##        設定圖片
#        with open("richmenu.jpg", 'rb') as f:
#            line_bot_api.set_rich_menu_image(rich_menu_list[1].rich_menu_id, "image/jpeg", f)
#        req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(rich_menu_list[1].rich_menu_id),headers=headers)
#        _id = rich_menu_list[1].rich_menu_id
#        line_bot_api.link_rich_menu_to_user(event.source.user_id, _id)
#        print(req.text)
    elif event.message.text == '大學':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/W4RoWAe.jpg',
                size='full',
                aspect_ratio='11:5',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                        
                    # title
                    TextComponent(text='宜蘭大學', weight='bold', size='xl'),
                    # review
                    TextComponent(
                            text='大學是念商管科系，在大三時期，自己興趣加上因緣際會接觸到JAVA，發現用程式碼做出成品會讓我感動，所以那時就下定決心要往資訊領域發展，期間自學java及Android app應用程式，對於手機App以及java等程式語言很有興趣，在大學期間有做出基本的購物車及多人聊天室app等等，但是都是自己練功為主，最後為了精進資訊基礎，決定就讀資訊管理研究所，期待能更加專研資訊技術。',
                            size='xs',wrap=True
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '自學JAVA',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '自學Android APP',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '擔任班級代表',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '於當完兵後準備資訊相關研究所',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            )
                        ],

                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=PostbackAction(label='瀏覽其他stage', text='下方的rich menu也可以點選喔~',data='else')
                    )
                ]
            )
        )   
        message = FlexSendMessage(alt_text="undergraduate", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
       
    elif event.message.text == '研究所':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/a7MHkWj.jpg',
                size='full',
                aspect_ratio='11:5',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                        
                    # title
                    TextComponent(text='中正大學', weight='bold', size='xl'),
                    # review
                    TextComponent(
                            text='到了研究所就讀後，還是需要持續的自學與定期追蹤軟體開發技術相關消息，因而開始自學接觸到這幾年蠻火熱的LineBot，我有一些相關的程式碼與心得放在我的部落格，而目前在吳帆教授的指導之下研究LINE BOT結合AI的應用。',
                            size='xs',wrap=True
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '自學LINE BOT',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '自學Python',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '參加朝陽大學辦的微創星球資訊創新比賽，LINEBOT實作問卷系統為主題寫一個小小BOT，簡單來說就是改善現行店家問卷填寫方式，最後得到第四名佳作',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '這學期在國泰世華銀行資訊部實習，學習系統開發流程與小工具的實作',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            )
                        ],

                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=PostbackAction(label='瀏覽其他stage', text='下方的rich menu也可以點選喔~',data='else')
                    )
                ]
            )
        )   
        message = FlexSendMessage(alt_text="graduate", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    elif event.message.text == '出社會':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://i.imgur.com/EaX6ScF.jpg',
                size='full',
                aspect_ratio='11:5',
                aspect_mode='cover'
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                        
                    # title
                    TextComponent(text='進入LINE實習', weight='bold', size='xl'),
                    # review
                    TextComponent(
                            text='看到LINE開放了Tech Fresh的實習機會，我知道我一定要把握這機會，不管有沒有被錄取，在過去半年之間，我已經與LINE BOT朝曦相處，我喜歡LINE的創意及提供更強的API，而心中一直覺得日後Chatbot有機會來取代傳統APP，雖然Chatbot已經出來有段時間了，但我看好未來有強大的潛力，所以我會持續朝這方向前進。最後我發現到LINE是開放、負責及尊重的公司，現在已經過了第一階段履歷篩選了，對我來說就像是做夢一樣，能夠進入LINE公司，並與那麼多優秀的同事一起工作，不僅可以提升自己能力，更能提高自己視野並兼顧興趣!!!',
                            size='xs',wrap=True
                    ),
                    SeparatorComponent(),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = 'KaKa加油💪💪💪💪',
                                        size='xs',
                                        wrap=True,
                                        flex=8,
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '不要放棄💪💪💪💪',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '持續努力💪💪💪💪',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='horizontal',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='◾',
                                        size='md'
                                    ),
                                    TextComponent(
                                        text = '繼續學習💪💪💪💪',
                                        size='xs',
                                        wrap=True,
                                        flex=8
                                    )
                                ],
                            )
                        ],

                    ),
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    ButtonComponent(
                        style='primary',
                        height='sm',
                        action=PostbackAction(label='瀏覽其他stage', text='下方的rich menu也可以點選喔~',data='else')
                    )
                ]
            )
        )
        message = FlexSendMessage(alt_text='society', contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.message.text == '回主畫面':
        _id = os.getenv('first_richmenu',None)
        headers = {"Authorization":"Bearer {}".format(os.getenv('LINE_CHANNEL_ACCESS_TOKEN',None)),"Content-Type":"application/json"}
        req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/{}'.format(_id),headers=headers)
        line_bot_api.link_rich_menu_to_user(event.source.user_id, _id)
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
