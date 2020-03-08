import requests
import uuid
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from read_json import get_config

credentials = get_config("config_credentials")
config = get_config("config_private")

vk_session = vk_api.VkApi(token=config.get("group").get("token"))
upload = vk_api.VkUpload(vk_session)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id=config.get("group").get("id_group"))

# Переключение на пользователя
def UserSessionAuth():
    login = get_config("config_private").get("user").get("login")
    password = get_config("config_private").get("user").get("password")
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    return vk_session

# Скачивает фотографию пользователя
def getUserPhoto(event):
    id_group = config.get("group").get("id_group")
    img_data = 0
    code = False
    for i in range(len(credentials.get("photo_sizes"))):
        for j in range(len(event.object['message']['attachments'][0]['photo']['sizes'])):
            if event.object['message']['attachments'][0]['photo']['sizes'][j]['type'] == credentials.get("photo_sizes")[i]:
                img_data = requests.get(event.object['message']['attachments'][0]['photo']['sizes'][j]['url']).content
                code = True
                break
        if code:
            break
    if code == False:
        vk_session.method("messages.send", {"user_id": event.object["message"]["from_id"],
                                            "message": credentials.get("users").get("photo").get("size_error"),
                                            "random_id": 0})
        return
    id = uuid.uuid4()
    img_name = f'{id}.jpg'
    with open(f'media/{id_group}/user/' + img_name, 'wb') as userphoto:
        userphoto.write(img_data)
    print(event.object)

    # Отправление ответного сообщения пользователю (та же фотография)
    photo = upload.photo_messages(f'media/{id_group}/user/' + img_name)[0]
    attachments = list()
    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    vk_session.method('messages.send', {'user_id': event.object['message']['from_id'], 'random_id': 0,
                                        'attachment': ','.join(attachments)})

# Сохраняет фотографии с нового поста сообщества
def getWallPhoto(event):
    id_group = config.get("group").get("id_group")
    img_data = 0
    for i in range(len(event.object['attachments'])):
        if event.object['attachments'][i]['type'] == 'photo':
            code = False
            for j in range(len(credentials.get("photo_sizes"))):
                for k in range(len(event.object['attachments'][i]['photo']['sizes'])):
                    if event.object['attachments'][i]['photo']['sizes'][k]['type'] == credentials.get("photo_sizes")[j]:
                        img_data = requests.get(event.object['attachments'][i]['photo']['sizes'][k]['url']).content
                        code = True
                        break
                if code:
                    break
            if code == False:
                continue
            id = uuid.uuid4()
            name_img = f'{id}.jpg'
            with open(f'media/{id_group}/' + name_img, 'wb') as photo:
                photo.write(img_data)
            print(event.object)
        else:
            break

# Скачивает все фотографии сообщества и добавляет в БД
def getAllAlbumPhotos():
    # Добавление в БД
    id_group = config.get("group").get("id_group")
    vk_session = UserSessionAuth()
    img_data = 0
    offset = 0
    while True:
        photos = vk_session.method('photos.getAll',
                               {'owner_id': -id_group, 'offset': offset, 'count': 200, 'photo_sizes': 0,
                                'no_service_albums': 0})
        for i in range(len(photos['items'])):
            code = False
            for j in range(len(credentials.get("photo_sizes"))):
                for k in range(len(photos['items'][i]['sizes'])):
                    if photos['items'][i]['sizes'][k]['type'] == credentials.get("photo_sizes")[j]:
                        img_data = requests.get(photos['items'][i]['sizes'][k]['url']).content
                        code = True
                        break
                if code:
                    break
            if code == False:
                continue
            id = uuid.uuid4()
            img_name = f'{id}.jpg'
            with open(f'media/{id_group}/' + img_name, 'wb') as photo:
                photo.write(img_data)
        if len(photos['items']) != 200:
            break
        else:
            offset += 200

    print('"AlbumPhoto" downloading is completed')

# Скачивает новые фотографии и добавляет в БД
def getNewPhotos(event=None):
    img_data = 0
    id_group = config.get("group").get("id_group")
    vk_session = UserSessionAuth()

    if event == None:
        # Определение фото, которого нет в БД, скачивает и добавляет
        return
    else:
        # Скачивает фотографию и добавляет в БД
        code = False
        for i in range(len(credentials.get("photo_sizes"))):
            for j in range(len(event.object['sizes'])):
                if event.object['sizes'][j]['type'] == credentials.get("photo_sizes")[i]:
                    img_data = requests.get(event.object['sizes'][j]['url']).content
                    code = True
                    break
            if code:
                break
        if code == False:
            return
        id = uuid.uuid4()
        img_name = f'{id}.jpg'
        with open(f'media/{id_group}/' + img_name, 'wb') as photo:
            photo.write(img_data)
        print(event.object)

# Проверка изменений фотографий в сообществе через БД
def ControlAlbumPhotos():
    # Проверка изменений в БД
    # 0 - нет изменений
    # 1 - есть изменения
    # 2 - нет фотографий сообщества
    return 2;

# Функция, создает интерактивные кнопки в диалоге
def Create_board(text=None):
    keyboard = VkKeyboard(one_time=True)
    if text:
        return keyboard.get_empty_keyboard()
    keyboard.add_button('Search photos', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Close keyboard', color=VkKeyboardColor.NEGATIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard
