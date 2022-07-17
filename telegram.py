import telebot
import re
import httpx
from telebot.types import InputMediaPhoto



Token = ' '#telebot的token
bot = telebot.TeleBot(Token, parse_mode=None)


class nga():
    uid = ''#ngaPassportUid
    cid = ''#ngaPassportCid
    url = 'https://bbs.nga.cn/read.php'
    imgUrl = 'https://img.nga.178.com/attachments/'

    def __init__(self):
        pass

    def get_tid(self, tid):
        headers = {"User-agent": "Nga_Official/80023"}  # 请求头
        cookies = {
            "ngaPassportUid": self.uid,
            "ngaPassportCid": self.cid}  # cookie
        params = (("tid", tid), ("lite", "js"))  # 参数
        get = httpx.get(
            self.url,
            params=params,
            headers=headers,
            cookies=cookies,
        )  # 请求
        get.encoding = "GBK"  # 编码
        pl = (
            get.text.replace("   ", "")
        )  # 替换
        a = pl[33:]
        user_text = re.findall(
            r'"__R":{"0":{"content":"(.+?)","alterinfo"', a, flags=re.S)
        send_text = str(user_text).replace("['", "").replace( "']", "").replace('<br/>', '\n').replace('</br>', '\n')

        title_text = re.findall(r'"subject":"(.+?)","type"', a)
        title = str(title_text).replace("['", "").replace("']", "")

        img_list = re.findall(r'img](.+?)\[/img]', send_text, flags=re.S)
        for result in img_list:
                send_text = send_text.replace('[img]' + result + '[/img]', '')
        if len(img_list)==0:                              #判断是否存在图片
            media = None
        else:
            media = []                    #创建图片资源组
            all = title+"\n"+send_text
            for oo in img_list:
                img_name = oo[2:]
                img_url = self.imgUrl + img_name
                media.append(
                    InputMediaPhoto(img_url, all)
                )
                all = ""
                # 发送
        return title, send_text, media


@bot.message_handler()
def start(message):
    tid = message.text
    chat_id = message.chat.id
    ngad = nga()
    title, send_text, media = ngad.get_tid(tid)

    if media == None or len(media)==0:
        bot.send_message(chat_id, str(title + '\n' + send_text))
    else:
        bot.send_media_group(chat_id, media)


bot.infinity_polling()
