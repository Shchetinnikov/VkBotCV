import VkBot_photos
from VkBot_photos import credentials, config
from VkBot_photos import VkBotEventType, VkBotLongPoll, vk_api, vk_session, longpoll

# БД хранит информацию о всех фотографиях сообщества

if __name__ == '__main__':
    # Проверка наличия или изменения фотографий в сообществе
    if VkBot_photos.ControlAlbumPhotos() == 1:
        VkBot_photos.getNewPhotos()
    elif VkBot_photos.ControlAlbumPhotos() == 2:
        VkBot_photos.getAllAlbumPhotos()

    for event in longpoll.listen():
        # Обработка сообщений пользователей
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.object['message']['text'].lower()
            if len(event.object['message']['attachments']) != 0:
                if len(event.object['message']['attachments']) == 1:
                    VkBot_photos.getUserPhoto(event)
                else:
                    vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                            'message': config.get('users').get('photo').get('warning'),
                                                            'random_id': 0})
            elif text == 'search photos':
                vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                        'message': config.get('users').get('photo').get('warning'),
                                                        'random_id': 0})
            elif text == 'close keyboard':
                keyboard = VkBot_photos.Create_board(text)
                vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                        'message': config.get('users').get('end'),
                                                        'random_id': 0, 'keyboard': keyboard})
            elif text != '':
                keyboard = VkBot_photos.Create_board()
                vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                       'message': config.get('users').get('start'), 'random_id': 0, 'keyboard': keyboard})

        # Сохранение новых фотографий в альбомах сообщества
        if event.type == VkBotEventType.PHOTO_NEW:
            VkBot_photos.getNewPhotos(event)
        # Сохранение фотографий с нового поста сообщества
        if event.type == VkBotEventType.WALL_POST_NEW:
            VkBot_photos.getWallPhoto(event)
