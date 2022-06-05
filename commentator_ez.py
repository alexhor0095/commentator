from pyrogram import Client  # телеграм клиент
import shelve  # запись информации в файл
import random  # для выбора случайного элеменита из списка
import time  # для выбора случайного элеменита из списка

# Данные приложения телеграм (можно создать на my.telegram.org)
api_id = 14677815
api_hash = "30366a9e2c254ce4a385255943d068c2"
phone_number = '+79613459451'  # телефонный номер аккаунта в телеграме

PUBLICS = [
    'nemorgenshtern',
    'anatoly_nesmiyan'
]  # паблики через запятую

# Варианты текстов сообщений через запятую
TEXTS = [
    'интересно',
    'мм, нормалды',
    'жесть',
    'dsad'
]

COMMENT_EVERY_N = 1  # комментируем каждое N собщение
# если равно 1, комментируем каждое сообщение
# если равно 3, комментируем каждое третье
# если равно 5, комментируем каждое пятое ... итд

# список обработанных сообщений
processed_messages = shelve.open('processed_messages.db',  # имя файла, куда писать
                                 writeback=True)

# создаем клиент телеграма
app = Client("commentator", api_id, api_hash,
             phone_number=phone_number)

with app:
    while True:
        for public in PUBLICS:
            public = app.get_chat(public)  # ищем паблик по нику
            chat = public.linked_chat  # связанный чат обсуждений паблика

            for msg in app.get_chat_history(chat.id, limit=100):
                # фильтруем только авторепосты из паблика
                if (msg.from_user is None  # если сообщение не имеет автора
                        # и это репост из паблика (проверка по id)
                        and public is not None
                        and msg.forward_from_chat is not None
                        and msg.forward_from_chat.id == public.id
                ):
                    if msg.forward_from_message_id % COMMENT_EVERY_N != 0:
                        print(f'Пропускаем message_id={msg.message_id},'
                              f' так как комментируе каждое {COMMENT_EVERY_N}')
                        continue
                    # проверяем, есть ли в списке обработанных сообщений этот айди
                    # чтобы не комментировать по несколько раз один пост
                    if (str(msg.forward_from_message_id)+str(chat.id)) in processed_messages:
                        print(f'Пропускаем уже обработанное сообщение  {msg.forward_from_message_id}'+f' из  чата {msg.chat.title}')
                        continue
                    # пишем в список обработанных айди этого сообщения
                    processed_messages[str(msg.forward_from_message_id)+str(chat.id)] = True

                    print(f'Обработка message_id={msg.forward_from_message_id}')

                    text = random.choice(TEXTS)  # выбираем случайный текст из списка
                    app.send_message(chat.id, text,  # отправляем текст в чат
                                     reply_to_message_id=msg.id)

                    # для того, чтоб не оставлять больше одного коммента за 5 минут
                    break  # выходим из перебора сообщений, если оставили коммент

        print('Ставим на паузу')
        time.sleep(10)






