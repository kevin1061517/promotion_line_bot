# promotion_line_bot
簡介:
-------  
我實作的這個LINE BOT不具有自然語言理解能力(NLU)，因為我想呈現出最單純的LINE BOT，來證明利用LINE所提供的Message API，就可以實作出一個Chatbot來promote我自己，簡單來說我就是藉由預先設定好的If-else條件式、對話選單及回應腳本所建構出的Rule-Based Chatbot。不依靠Google的dialogflow來實作Chatbot，我完全依靠自己的程式碼以及完善的Message API(像是Flex message、richmenu、QuickReply、LIFF.....)希望可以藉著這Chatbot讓大家認識到我，也達到Promote我自己的效益。

內容: 
------- 
當一開始進去時會看到下方的Richmenu，如下介紹
![image](https://i.imgur.com/RRXy2HY.png)

1.`KaKa world`為進入我自己的歷程作介紹，當中有利用rich menu的API來做rich menu的轉換，讓user更輕易看出之中的變化，而且利用rich menu可以更清楚呈現我想要表達的內容。

2.`Hobby`為我自己的興趣彙整，並利用python爬蟲技術，爬取一些資訊來清楚呈現出來。

3.`Menu`Menu為彙整所有重要的選項，都集中在這個Menu裡面，但裡面多了獨特的兩個選項，一個為用LIFF開啟我的blog，二為讓user傳訊息給我本人，這部分期待能收到鼓勵的話或是更多建議給我。

4.`Github`為用LIFF開啟我自己的GitHub來給user查看。

檔案: 
------- 
1. `main_Bot.py`    加入line bot api來處理input進來的user訊息
2. `web_crawler.py` 裡面的方法(function)來處理爬蟲相關問題。

QR-code: 
------- 
![image](https://github.com/kevin1061517/promotion_line_bot/blob/master/QR_code.png)
