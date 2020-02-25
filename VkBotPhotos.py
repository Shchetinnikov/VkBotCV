import requests
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import vk_api
from config import login, password, token, id_group


def SessionAuth(value):
    global vk_session, upload, session_api, longpoll
    if value == 1:
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
    else:
        vk_session = vk_api.VkApi(token=token)
    upload = VkUpload(vk_session)
    session_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=id_group)


# Функция обработки фотографии пользователя
def UserPhoto(event):
    global count_userphoto
    field = 0
    max_s = 0
    for i in range(len(event.object['message']['attachments'][0]['photo']['sizes'])):
        width = event.object['message']['attachments'][0]['photo']['sizes'][i]['width']
        height = event.object['message']['attachments'][0]['photo']['sizes'][i]['height']
        if height + width > max_s:
            max_s = width + height
            field = i
    img_data = requests.get(event.object['message']['attachments'][0]['photo']['sizes'][field]['url']).content
    img_name = f'userphoto{count_userphoto}.jpg'
    with open(f'media/id{id_group}/user/' + img_name, 'wb') as userphoto:
        userphoto.write(img_data)
    count_userphoto += 1
    print(event.object)

    # Отправление ответного сообщения пользователю (та же фотография)
    photo = upload.photo_messages(f'media/id{id_group}/user/' + img_name)[0]
    attachments = list()
    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    vk_session.method('messages.send', {'user_id': event.object['message']['from_id'], 'random_id': 0,
                                        'attachment': ','.join(attachments)})


def GroupAlbumPhoto(event=None):
    global count_photo
    if event == None:
        photos = vk_session.method('photos.getAll',
                                       {'owner_id': -id_group, 'offset': 0, 'count': 200, 'photo_sizes': 0,
                                        'no_service_albums': 0})
        for i in range(photos['count']):
            max_s = 0
            for k in range(len(photos['items'][i]['sizes'])):
                width = photos['items'][i]['sizes'][k]['width']
                height = photos['items'][i]['sizes'][k]['height']
                if (height + width) > max_s:
                    max_s = width + height
                    field = k
            img_data = requests.get(photos['items'][i]['sizes'][field]['url']).content
            img_name = f'photo{count_photo}.jpg'
            with open(f'media/id{id_group}/' + img_name, 'wb') as photo:
                photo.write(img_data)
            count_photo += 1

        print('"AlbumPhoto" downloading is completed')
    else:
        max_s = 0
        for i in range(len(event.object['sizes'])):
            width = event.object['sizes'][i]['width']
            height = event.object['sizes'][i]['height']
            if width + height > max_s:
                max_s = width + height
                field = i
        img_data = requests.get(event.object['sizes'][field]['url']).content
        img_name = f'photo{count_photo}.jpg'
        with open(f'media/id{id_group}/' + img_name, 'wb') as photo:
            photo.write(img_data)
        count_photo += 1
        print(event.object)


# Функция, сохраняет фотографии с нового поста сообщества
def GroupWallPhoto(event):
    global count_photo
    for i in range(len(event.object['attachments'])):
        if event.object['attachments'][i]['type'] == 'photo':
            length = len(event.object['attachments'][i]['photo']['sizes']) - 1
            img_data = requests.get(event.object['attachments'][i]['photo']['sizes'][length]['url']).content
            name_img = f'photo{count_photo}.jpg'
            with open(f'media/id{id_group}/' + name_img, 'wb') as photo:
                photo.write(img_data)
            count_photo += 1
            print(event.object)
        else:
            break

# Функция, создает интерактивные кнопки в диалоге
def Create_board(text=None):
    keyboard = VkKeyboard(one_time=True)
    if text:
        return keyboard.get_empty_keyboard()
    keyboard.add_button('Найти фотографии', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Закрыть клавиатуру', color=VkKeyboardColor.NEGATIVE)
    keyboard = keyboard.get_keyboard()
    return keyboard


# Переменные
count_photo = 0
count_userphoto = 0
field = 0
