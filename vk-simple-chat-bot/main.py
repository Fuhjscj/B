import random
import logging
import time
from pathlib import Path

import yaml
import requests
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from gtts import gTTS

from functions import get_random_file, get_weather

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR.joinpath("config.yaml")
IMG_DIR = BASE_DIR.joinpath("img")
VIDEO_DIR = BASE_DIR.joinpath("video")
MUSIC_DIR = BASE_DIR.joinpath("music")
DOC_DIR = BASE_DIR.joinpath("documents")

# Считываем данные с конфига
with open(CONFIG_PATH, encoding="utf-8") as ymlFile:
    config = yaml.load(ymlFile.read(), Loader=yaml.Loader)

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger('vk_api')
logger.disabled = True

# Авторизация бота
authorize = vk_api.VkApi(token=config["group"]["group_token"])

longpoll = VkBotLongPoll(authorize, group_id=config["group"]["group_id"])
bot_upload = VkUpload(authorize)
bot = authorize.get_api()

# Авторизация в пользователя
vk_session = vk_api.VkApi(token=config["user"]["user_token"])

vk = vk_session.get_api()
vk_upload = VkUpload(vk_session)

logging.info("Авторизация прошла успешно")

global deita
delta = round(time.time() - message.date, 2)
    if delta < 0:
        delta = "777"

class Utils:
    def get_random_member(self, chat_id):
        """Возвращает id случайного участника беседы"""
        members = bot.messages.getConversationMembers(
            peer_id=2000000000 + chat_id,
            group_id=config["group"]["group_id"]
        )["items"]
        member_id = random.choice(members)["member_id"]
        return member_id

    def get_username(self, user_id):
        user_info = vk.users.get(user_ids=user_id)[0]
        username = "{} {}".format(
            user_info["first_name"],
            user_info["last_name"]
        )
        return f"[id{user_id}|{username}]"

    def get_group_name(self, group_id):
        group_info = vk.groups.getById(group_id=-group_id)[0]
        return f"[club{group_info['id']}|{group_info['name']}]"


class VkBot:
    def write_message(self, message="", attachment=""):
        """Отправляем в беседу сообщение."""
        bot.messages.send(
            chat_id=self.chat_id,
            message=message,
            attachment=attachment,
            random_id=get_random_id()
        )
	
    def say_check(self):
        message = f"✅На месте"
	Ping: {delta}
        self.write_message(message=message)
         
		
    def say_ferm(self):
        global x
        x = random.randint(1,50)
        global y
        y =  x
        message = f"✅ Зачёт +{y} 🍬  капнуло на счёт"
	Ping: {delta} 
        self.write_message(message=message)    
    
    def say_info(self):
        user_info = vk.users.get(user_id=self.sender_id)[0]
        username = user_info["first_name"]
        usernam = user_info["last_name"]
        y = x
	balans = 0
        balans = balans + y
        message = f"""
👤 Пользователь {username} {usernam}
💰 Баланс: {balans} 🍬
Ping: {delta}"""
	
        self.write_message(message=message)
                        
    def say_commands(self):
        message = f"""
Мои команды:
В начале каждой(кроме "ку, проверка,бот команды") команды ставится префикс (".н").
ку-Приветствие(голососое или писменое).
пикча-Выдаёт рандомную картинку из архива.
видосик-Выдаёт рандомное видио из архива.
проверка-Проверка бота на работоспособность.
кто-Выбирает рандомного человека.
погода-погода в данном городе.
бот команды-Список команд для юзеров.

Ping: {delta}"""
        self.write_message(message=message)
        
    def say_hello(self):
        user_info = vk.users.get(user_id=self.sender_id)[0]
        username = user_info["first_name"]
        usernam = user_info["last_name"]
        message = f"Привет {username}. Чтобы узнать мои команды напиши, бот команды!"
        x = random.randint(1, 2)
        if x == 0:
            # Отправляем сообщение в беседу
            self.write_message(message=message)
        else:
           # Отправляем голосовое сообщение в беседу
            tts = gTTS(text=message, lang="ru", lang_check=True)
            file_path = BASE_DIR.joinpath("audio.mp3")
            tts.save(file_path)

            self.send_file("audio.mp3", file_type="audio_message")

            file_path.unlink()

    def send_file(self, file, file_type):
        attachment = ""
        if file_type == "photo":
            """Загружаем фото на сервер Вконтакте."""
            response = bot_upload.photo_messages(
                photos=file,
                peer_id=2000000000 + self.chat_id
            )[0]
            attachment = "photo{}_{}".format(response["owner_id"], response["id"])
        elif file_type == "video":
            """Загружаем видео на сервер Вконтакте."""
            response = vk_upload.video(video_file=file, name="Видео")
            attachment = "video{}_{}".format(response["owner_id"], response["video_id"])
        elif file_type == "audio":
            """Загружаем аудиозапись на сервер Вконтакте."""
            song_data = str(file.name)[:-3].split(" - ")
            response = vk_upload.audio(
                audio = str(file),
                artist = song_data[0],
                title = song_data[1]
            )
            attachment = "audio{}_{}".format(response["owner_id"], response["id"])
        elif file_type == "audio_message":
            response = bot_upload.audio_message(
                audio="audio.mp3",
                peer_id=2000000000 + self.chat_id
            )["audio_message"]
            attachment = "doc{}_{}".format(response["owner_id"], response["id"])
        elif file_type == "doc":
            response = bot_upload.document_message(
                doc=file,
                title="doc",
                peer_id=2000000000 + self.chat_id
            )["doc"]
            attachment = "doc{}_{}".format(response["owner_id"], response["id"])
        self.write_message(attachment=attachment)

    def check_message(self, received_message):
        if received_message == "ку":
            self.say_hello()

        elif received_message == "н пикча":
            photo = get_random_file(IMG_DIR)
            self.send_file(
                file=str(photo),
                file_type="photo"
            )

        elif received_message == "н видосик":
            video = get_random_file(VIDEO_DIR)
            self.send_file(
                file=str(video),
                file_type="video"
            )

        elif received_message == "н аудио":
            audio = get_random_file(MUSIC_DIR)
            self.send_file(
                file=str(audio),
                file_type="music"
            )
         
        elif received_message == "н инфо":
          self.say_info()
        
        elif received_message == "н ферма":
          self.say_ferm()
              
        elif received_message == "проверка":
          self.say_check()
        
        elif received_message == "бот команды":
         self.say_commands()
        
        elif received_message ==  "н док":
            document = get_random_file(DOC_DIR)
            self.send_file(
                file=str(document),
                file_type="doc"
            )

        elif received_message[:6] == "н кто":
            member_id = utils.get_random_member(chat_id=self.chat_id)
            phrases = ["Я думаю, это ", "Однозначно это ", "Скорее всего, это ", "Это ты", "Звёзды говорят что,это "]
            message = random.choice(phrases)
            if message != "Это ты":
                if member_id > 0:
                    message += utils.get_username(member_id)
                else:
                    message += utils.get_group_name(member_id)
            self.write_message(message)

        elif received_message[:8] == "н погода":
            city = received_message[10:].lower().replace(" ", "-")
            weather_data = get_weather(city)

            print(weather_data)

            if weather_data:
                city = city[:1].upper() + city[1:]
                message = f"""
🌞Погода в городе {city} на сегодня 🌌🗺️🧭:
Температура: {weather_data['temp']}🌡
Восход: {weather_data['sunrise']} 🌅
Закат в: {weather_data['sunset']} 🌇
Давление: {weather_data['pressure']} мм 🐡
Влажность: {weather_data['humidity']} % 💧
Ветер: {weather_data['wind']} 🌪️

Ping: {delta}
"""
            else:
                message = "Блядь, Напиши город в ИМЕНИТЕЛЬНОМ ПАДЕЖЕ"

            self.write_message(message=message)


    def listen(self):
        """Отслеживаем каждое событие в беседе."""
        while True:
            try:
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message and event.message.get("text") != "":
                        received_message = event.message.get("text").lower()
                        self.chat_id = event.chat_id
                        self.sender_id = event.message.get("from_id")
                        self.check_message(received_message)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                # Перезагрузка серверов ВКонтакте
                print(e)
                logging.info("Перезапуск бота")

    def run(self):
        logging.info("Бот запущен")
        self.listen()


if __name__ == "__main__":
    vkbot = VkBot()
    utils = Utils()
    vkbot.run() 
