import telebot
from telebot.types import Message
from flask import Flask
import threading
import os
import time
from time import sleep
import sys
from colorama import Fore, Back, Style
import random
import requests
import json
from datetime import datetime, timedelta
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import BoundedSemaphore
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
threading = ThreadPoolExecutor(max_workers=int(100000))
bot_token = '' 
bot = telebot.TeleBot(bot_token)
processes = {
  "abc":{
    "9292":123
  }
}
chan_spam = {}
chan_schedu = {}
# điền
ADMIN_ID = '7148638872'
ID_GROUP = '5254000161' # bỏ dấu trừ
link_gr = "https://t.me/+L8L70n3_UpYyZWE1"
web_key = "https://hoangtapcode123.github.io/showkey/?key="
user_bot = "@spamgasmsbot"
admin_user = "@hoanglovl"
zalo = "https://zalo.me/g/tuhkfd330"
delay_vip = 400
delay_free = 300
# schedule
def sched():
  while True:
    schedule.run_pending()
    time.sleep(1)

threading.submit(sched)
print("load schedule thành công")
# hàm 
def spamsche(phone_number,lap,message,key,name_sche):
  file_path = os.path.join(os.getcwd(), "smsvip.py")
  process = subprocess.Popen(["python", file_path, phone_number, lap])
  phone_number = phone_number[:4] + "*****" + phone_number[-1]
  text = f'<strong>🚀 Yêu Cầu Tấn Công Thành Công Đặt lịch Cho {getfullname(message)} 🚀</strong>\n<blockquote>┌ Bot 👾: {user_bot} \n├ Số Tấn Công 📱: [ {phone_number} ]\n├ Lặp lại : {lap}\n├ Chủ sở hữu 👑: {admin_user}\n├ Zalo:{zalo}\n└ Key : {key}</blockquote>'
  bot.send_video(message.chat.id, video=getvideo(), caption=text, supports_streaming=True,parse_mode='HTML')
  schedule.clear(name_sche) 
  del chan_schedu[name_sche]
  


def getvideo():
  try:
    return random.choice(requests.get("https://raw.githubusercontent.com/nguyenductai206/list/refs/heads/main/listvideo.json").json())
  except:
    pass

def xoatn(message,dl): 
  time.sleep(dl)
  bot.delete_message(message.chat.id, message.message_id)
  
def getfullname(message):
  try:
    a = message.from_user.first_name + " " + message.from_user.last_name
    return a
  except:
    return "Chưa xác định"
def checkgroup(message):
  if message.chat.type == "supergroup" and message.chat.id == -int(ID_GROUP):
    return True
  else:
    full_name = getfullname(message)
    bot.send_message(message.chat.id, f"<b>🗺️ Chào mừng {full_name} đến với bot spam sms trên telegram !\nNhấp vào link bên dưới để chuyển sang nhóm\n<blockquote >Link: {link_gr}</blockquote> </b>", parse_mode='HTML')
    return False

def TimeStamp():
    now = str(datetime.date.today())
    return now



@bot.message_handler(commands=['key'])
def key(message):
  if not checkgroup(message):return
  if len(message.text.split()) == 1:
    bot.reply_to(message, '<strong>VUI LÒNG NHẬP KEY ĐÚNG FORM.</strong>\nví dụ : /key abc134',parse_mode="HTML")
    return

  user_id = message.from_user.id
  key = message.text.split()[1]
  username = message.from_user.username
  expected_key = "sms" + str(int(message.from_user.id) * int(datetime.date.today().day) - 126 * int(datetime.date.today().day))
  if key == expected_key:
    bot.reply_to(message, 'KEY HỢP LỆ. BẠN ĐÃ ĐƯỢC PHÉP SỬ DỤNG LỆNH /spam.')
    fi = open(f'./user/{datetime.date.today().day}/{user_id}.txt',"w")
    fi.write("")
    fi.close()
  else:
    bot.reply_to(message, 'KEY KHÔNG ĐÚNG VUI LÒNG DÙNG /getkey để lấy key')


@bot.message_handler(commands=['getkey'])
def startkey(message):
  if not checkgroup(message):return
  bot.reply_to(message, text='VUI LÒNG ĐỢI TRONG GIÂY LÁT!')
  key = "sms" + str(int(message.from_user.id) * int(datetime.date.today().day) - 126 * int(datetime.date.today().day))
  key = web_key + key
  #url_key = requests.get("https://partner.8link.io/api/public/gen-shorten-link?apikey=9aed18d301c366b2f369e2cad0aeac88cc2ba7871b4637b4b3eddfdd7a23ad42&url=" + key).json()["shortened_url"]
  text = f'''
- LINK LẤY KEY <i>{TimeStamp()}</i>  LÀ: {key} -
- KHI LẤY KEY XONG, DÙNG LỆNH /key &lt;key&gt; ĐỂ TIẾP TỤC -
    '''
  bot.reply_to(message, text,parse_mode="HTML")

@bot.message_handler(commands=['spam'])
def spam(message):
  if not checkgroup(message):return
  user_id = message.from_user.id
  if not os.path.exists(f"./user/{datetime.date.today().day}/{user_id}.txt"):
    bot.reply_to(message, 'Dùng /getkey để lấy key và dùng /key để nhập key hôm nay')
    return
  if len(message.text.split()) == 1:
    bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
    return
  if len(message.text.split()) == 2:
    bot.reply_to(message, 'Thiếu dữ kiện !!!')
    return
  lap = message.text.split()[2]
  if lap.isnumeric():
    if not (int(lap) > 0 and int(lap) <= 5):
      bot.reply_to(message,"Vui lòng spam trong khoảng 1-5.")
      return
  else:
    bot.reply_to(message,"Sai dữ kiện !!!")
    return
  phone_number = message.text.split()[1]
  if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$",phone_number):
    bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
    return
  if phone_number in ["0365956335"]:
    bot.reply_to(message,"Spam cái đầu buồi tao huhu")
    return
  if str(message.from_user.id) in chan_spam:
    dem = int(time.time()) - int(chan_spam[str(message.from_user.id)])
    if dem <= delay_free:
      bot.reply_to(message,f"Vui lòng chờ {delay_free - dem} giây cho lần spam tiếp theo")
      return
    
  file_path = os.path.join(os.getcwd(), "sms.py")
  process = subprocess.Popen(["python", file_path, phone_number, lap])
  if str(message.from_user.id) in processes:
    try:
      if phone_number in processes[str(message.from_user.id)]:
        processes[str(message.from_user.id)][phone_number].kill()
        processes[str(message.from_user.id)][phone_number] = process
      else:
        processes[str(message.from_user.id)][phone_number] = process
    except Exception as e:
      print(e)
  else:
    processes[str(message.from_user.id)] = {
      phone_number : process
    }
  phone_number = phone_number[:4] + "*****" + phone_number[-1]
  text = f'<strong>🚀 Gửi Yêu Cầu Tấn Công Thành Công Cho {getfullname(message)} 🚀</strong>\n<blockquote>┌ Bot 👾: {user_bot} \n├ Số Tấn Công 📱: [ {phone_number} ]\n├ Lặp lại : {lap}\n├ Chủ sở hữu 👑: {admin_user}\n├ Zalo: {zalo}\n└ Key : free</blockquote>'
  chan_spam[str(message.from_user.id)] = time.time()
  xoatn(message,2)
  bot.send_video(message.chat.id, video=getvideo(), caption=text, supports_streaming=True,parse_mode='HTML')



@bot.message_handler(commands=['vipspam'])
def vipspam(message):
  if not checkgroup(message):return
  user_id = message.from_user.id
  if not os.path.exists(f"./vip/{user_id}.txt"):
    bot.reply_to(message, 'Bạn chưa đăng ký vip vui lòng liên hệ admin\nZalo : 0365956335')
    return
  fo = open(f"./vip/{user_id}.txt")
  data = fo.read().split("|")
  qua_khu = data[0].split('-')
  qua_khu = datetime.date(int(qua_khu[0]), int(qua_khu[1]), int(qua_khu[2]))
  ngay_hien_tai = datetime.date.today()
  so_ngay = int((ngay_hien_tai - qua_khu).days)
  if so_ngay < 0:
      bot.reply_to(message, 'Key Vip Cài Vào ngày khác')
      return
  if so_ngay >= int(data[1]):
    bot.reply_to(message, 'Key Vip Hết Hạn Vui Lòng ib Admin\nZalo : 0365956335')
    os.remove(f"./vip/{user_id}.txt")
    return
  if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
        return
  if len(message.text.split()) == 2:
    bot.reply_to(message, 'Thiếu dữ kiện !!!')
    return
  lap = message.text.split()[2]
  if lap.isnumeric():
    if not (int(lap) > 0 and int(lap) <= 10):
      bot.reply_to(message,"Vui lòng spam trong khoảng 1-10.")
      return
  else:
    bot.reply_to(message,"Sai dữ kiện !!!")
    return
  phone_number = message.text.split()[1]
  if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$",phone_number):
    bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
    return
  if phone_number in ["0365956335"]:
    bot.reply_to(message,"Spam cái đầu buồi tao huhu")
    return
  
  if str(message.from_user.id) in chan_spam:
    dem = int(time.time()) - int(chan_spam[str(message.from_user.id)])
    if dem <= delay_vip:
      bot.reply_to(message,f"Vui lòng chờ {delay_vip - dem} giây cho lần spam tiếp theo")
      return
  file_path = os.path.join(os.getcwd(), "smsvip.py")
  process = subprocess.Popen(["python", file_path, phone_number, lap])
  if str(message.from_user.id) in processes:
    try:
      if phone_number in processes[str(message.from_user.id)]:
        processes[str(message.from_user.id)][phone_number].kill()
        processes[str(message.from_user.id)][phone_number] = process
      else:
        processes[str(message.from_user.id)][phone_number] = process
    except Exception as e:
      print(e)
  else:
    processes[str(message.from_user.id)] = {
      phone_number : process
    }
  phone_number = phone_number[:4] + "*****" + phone_number[-1]
  text = f'<strong>🚀 Gửi Yêu Cầu Tấn Công Thành Công Cho {getfullname(message)} 🚀</strong>\n<blockquote>┌ Bot 👾: {user_bot} \n├ Số Tấn Công 📱: [ {phone_number} ]\n├ Lặp lại : {lap}\n├ Chủ sở hữu 👑: {admin_user}\n├ Zalo:{zalo}\n└ Key : vip</blockquote>'
  chan_spam[str(message.from_user.id)] = time.time()
  xoatn(message,2)
  bot.send_video(message.chat.id, video=getvideo(), caption=text, supports_streaming=True,parse_mode='HTML')

  
@bot.message_handler(commands=['scspamvip'])
def scspamvip(message):
  if not checkgroup(message):return
  user_id = message.from_user.id
  if not os.path.exists(f"./vip/{user_id}.txt"):
    bot.reply_to(message, 'Bạn chưa đăng ký vip vui lòng liên hệ admin\nZalo : 0365956335')
    return
  fo = open(f"./vip/{user_id}.txt")
  data = fo.read().split("|")
  qua_khu = data[0].split('-')
  qua_khu = datetime.date(int(qua_khu[0]), int(qua_khu[1]), int(qua_khu[2]))
  ngay_hien_tai = datetime.date.today()
  so_ngay = int((ngay_hien_tai - qua_khu).days)
  if so_ngay < 0:
      bot.reply_to(message, 'Key Vip Cài Vào ngày khác')
      return
  if so_ngay >= int(data[1]):
    bot.reply_to(message, 'Key Vip Hết Hạn Vui Lòng ib Admin\nZalo : 0365956335')
    os.remove(f"./vip/{user_id}.txt")
    return
  if len(message.text.split()) == 1:
        bot.reply_to(message, 'VUI LÒNG NHẬP SỐ ĐIỆN THOẠI ')
        return
  if len(message.text.split()) != 4:
    bot.reply_to(message, 'Thiếu dữ kiện !!!')
    return
  lap = message.text.split()[2]
  if lap.isnumeric():
    if not (int(lap) > 0 and int(lap) <= 10):
      bot.reply_to(message,"Vui lòng spam trong khoảng 1-10.")
      return
  else:
    bot.reply_to(message,"Sai dữ kiện !!!")
    return
  phone_number = message.text.split()[1]
  if not re.search("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$",phone_number):
    bot.reply_to(message, 'SỐ ĐIỆN THOẠI KHÔNG HỢP LỆ !')
    return
  if phone_number in ["0365956335"]:
    bot.reply_to(message,"Spam cái đầu buồi tao huhu")
    return
  if str(message.from_user.id) in chan_spam:
    dem = int(time.time()) - int(chan_spam[str(message.from_user.id)])
    if dem <= delay_vip:
      bot.reply_to(message,f"Vui lòng chờ {delay_vip - dem} giây cho lần spam tiếp theo")
      return
  try:
    name_sche = str(user_id) + str(phone_number)
    if name_sche in chan_schedu:
      bot.reply_to(message, "vui lòng đổi số khác trong khi số bạn đang gửi đã được lên lịch")
      return
    schedule.every().day.at(message.text.split()[3],"Asia/Ho_Chi_Minh").do(spamsche,phone_number,lap,message,"vip",name_sche).tag(name_sche)
    chan_schedu[name_sche] = "0"
  except Exception as e:
    bot.reply_to(message, 'Sai format gio:phut')
    print(e)
    print("_____________________________")
    return
  bot.reply_to(message,"thêm thành công vào lịch")
  chan_spam[str(message.from_user.id)] = time.time()


  
@bot.message_handler(commands=['stop'])
def stop(message):
  if not checkgroup(message):return
  if len(message.text.split()) != 2:
    bot.reply_to(message, 'VUI LÒNG NHẬP ĐÚNG ĐỊNH DẠNG /stop <sdt>\n ví dụ : /stop 0365957443')
    return
  phone_number = message.text.split()[1]
  if str(message.from_user.id) in processes:
    try:
      if phone_number in processes[str(message.from_user.id)]:
        processes[str(message.from_user.id)][phone_number].kill()
        del processes[str(message.from_user.id)][phone_number]
        phone_number = phone_number[:4] + "*****" + phone_number[-1]
        xoatn(message,2)
        bot.send_message(message.chat.id, f"<pre>Dừng thành công số {phone_number}</pre>",parse_mode="HTML")
      else:
        xoatn(message,2)
        bot.send_message(message.chat.id, "<pre>Số bạn chưa có trong danh sách chạy</pre>",parse_mode="HTML")
    except Exception as e:
      print(e)
  else:
    xoatn(message,2)
    bot.send_message(message.chat.id, "<pre>Bạn chưa có trong danh sách chạy</pre>",parse_mode="HTML")

    
@bot.message_handler(commands=['stopsc'])
def stopsc(message):
  if not checkgroup(message):return
  if len(message.text.split()) != 2:
    bot.reply_to(message, 'VUI LÒNG NHẬP ĐÚNG ĐỊNH DẠNG /stopsc <sdt>\n ví dụ : /stopsc 0365957443')
    return
  phone_number = message.text.split()[1]
  name_sche = str(message.from_user.id) + str(phone_number)
  if name_sche not in chan_schedu:
    bot.reply_to(message, "số này chưa có trong lịch")
    return
  try:
    schedule.clear(name_sche)
    phone_number = phone_number[:4] + "*****" + phone_number[-1]
    xoatn(message,2)
    bot.send_message(message.chat.id, f"xóa lịch thành công số {phone_number}")
    del chan_schedu[name_sche]
  except Exception as e:
    print("lỗi stop schedule")
    print(e)
  
  
  
@bot.message_handler(commands=['help'])
def help(message):
  if not checkgroup(message):return
  text = f"""
  <b>Welcome to <i>my bot!</i></b>
<u>Đây là các lệnh của bot :</u>
  <code>/help</code> - Xem các lệnh.
  <code>/getkey</code> - Lấy key.
  <code>/key &lt;key&gt;</code> - Nhập key để mở khóa các tính năng bot.
  <code>/spam &lt;sdt&gt; &lt;solan&gt;</code> - spam sms call.
  <code>/vipspam &lt;sdt&gt; &lt;solan&gt;</code> - spam sms call bản vip.
  <code>/scspamvip &lt;sdt&gt; &lt;solan&gt; &lt;gio:phut&gt;</code> - spam sms call bản vip.
  <code>/stop &lt;sdt&gt;</code> - Dừng spam 1 số điện thoại của bạn đang chạy, <pre>không thể dừng cho /scspamvip</pre>.
  <code>/stopsc &lt;sdt&gt;</code> - Dừng spam 1 số điện thoại lên lịch của bạn.
  <code>/them</code> - admin.
  <code>/check</code> - admin.
  <code>/mua</code> - mua hoặc thuê bot.
  ──────────────────────────
  <a href="{zalo}">Bấm vào đây để tham gia group zalo.</a>
  """
  bot.send_message(message.chat.id, text,parse_mode="HTML")
    
# Phần Flask để chạy trên Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Telegram đang chạy!"

def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
# khoir dong lai bot
@bot.message_handler(commands=['check'])
def check(message):
  if not checkgroup(message):return
  user_id = message.from_user.id
  if str(user_id) != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
    return
  try:
    soluong = os.listdir(f"./user/{datetime.date.today().day}")
    bot.reply_to(message,f"Số lượng nhập key hôm nay : {len(soluong)}")
  except Exception as e:
    print(e)
    print("_____________________________")
    return


@bot.message_handler(commands=['them'])
def them(message):
  if not checkgroup(message):return
  user_id = message.from_user.id
  if str(user_id) != ADMIN_ID:
    bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
    return
  try:
    idvip = message.text.split(" ")[1]
    ngay = message.text.split(" ")[2]
    hethan = message.text.split(" ")[3]
    fii = open(f"./vip/{idvip}.txt","w")
    fii.write(f"{ngay}|{hethan}")
    bot.reply_to(message, f'Thêm Thành Công {idvip} Làm Vip')
  except Exception as e:
    bot.reply_to(message, f'Thêm Không Thành Công {idvip} Làm Vip')
    print(e)
    print("_____________________________")
    

# mua
@bot.message_handler(commands=['start'])
def start(message):
  if message.chat.type == "private":
    full_name = getfullname(message)
    bot.send_message(message.chat.id, f"<b>🗺️ Chào mừng {full_name} đến với bot spam sms trên telegram !\nNhấp vào link bên dưới để chuyển sang nhóm\n<blockquote >Link: {link_gr}</blockquote> </b>", parse_mode='HTML')


@bot.message_handler(commands=['mua'])
def mua(message):
  if not checkgroup(message):return
  reply_text = 'Giá cả của các gói dịch vụ tất cả đều chat admin:\n'
  reply_text += '────────────────────────\n'
  reply_text += '┌ Gói /spam: 20k/1 tháng\n'
  reply_text += '└ Mua suộc bot giống bot 150k Không giới hạn\n'
  reply_text += '────────────────────────'
  bot.reply_to(message, f"<blockquote>{reply_text}</blockquote>",parse_mode="HTML")


# lenh lo 

bot.infinity_polling()
