import requests
import time
from datetime import datetime

TOKEN = "TELEGRAM-BOT-TOKEN"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
send_message_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Son alınan update_id'yi tut
last_update_id = None

# Mesajın gönderileceği chat_id (belirttiğiniz ID)
recipient_chat_id = "XXXXXXXXXX"  # Buraya hedef ID'yi yaz

def log_message(user_id, message):
    filename = f"logs/{user_id}.txt"  # Kullanıcı ID'ye özel dosya
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Şu anki tarih ve saat
    new_entry = f"{now} - {message}\n"

    # Eski içeriği oku
    try:
        with open(filename, "r", encoding="utf-8") as file:
            old_content = file.read()
    except FileNotFoundError:
        old_content = ""  # Eğer dosya yoksa boş bırak

    # Yeni içeriği en üste ekle
    updated_content = new_entry + old_content

    # Dosyayı yeniden yaz (overwrite)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(updated_content)
        
while True:
    # Yeni güncellemeleri al
    params = {}
    if last_update_id:
        params['offset'] = last_update_id + 1  # Yeni güncellemeler için offset kullan

    response = requests.get(url, params=params).json()

    if response["ok"]:
        for result in response["result"]:
            
            
            message = result["message"]
            user_id = message["from"]["id"]
            username = message["from"]["username"]
            text = message["text"]
            update_id = result["update_id"]
            
            if text[0]!="/":
                now = datetime.now()
                zaman = now.strftime("%d-%m-%Y %H:%M:%S")
                
                # Gelen mesaj ve kullanıcı adıyla bir metin oluştur
                reply_text = f"Yeni mesaj geldi:\n\nKullanıcı: @{username}\nMesaj: {text}\nID: /{user_id}x"

                # Belirtilen ID'ye mesajı gönder
                params = {
                    'chat_id': recipient_chat_id,
                    'text': reply_text
                }
                requests.get(send_message_url, params=params)

                # Son update_id'yi kaydet
                last_update_id = update_id
                print("Üye/Misafir:","|",text,"|",zaman)
                
                log_message(recipient_chat_id, text)

            elif text[0] =="/" and str(user_id)=="XXXXXXXXXX":
                now = datetime.now()
                zaman = now.strftime("%d-%m-%Y %H:%M:%S")
                reply_text = f"Yeni mesaj geldi:\n\nKullanıcı: @{username}\nMesaj: {text}\nID: /{user_id}"
                
                
                # 'x' karakterine kadar olan kısmı almak
                karsi_id = text.split('x')[0]
                temizlenmis = karsi_id.replace("x", "")  # 'a' harflerini sil
                temizlenmis_id = karsi_id.replace("/", "")  # 'a' harflerini sil

##                print(temizlenmis_id)
                
                cevap = text.split('x')[1].strip()
                print("Dijital Kazanç:","|",cevap,"|",zaman)
                
                params = {
                    'chat_id': temizlenmis_id,
                    'text': cevap
                }
                requests.get(send_message_url, params=params)
                last_update_id = update_id
                
                log_message(temizlenmis_id, cevap)
    # Her döngüde küçük bir bekleme süresi ekle
    time.sleep(1)
