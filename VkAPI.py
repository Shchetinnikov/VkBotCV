import VkBotPhotos as VkBot

# Пока реализовано для одного паблика
if __name__ == '__main__':
    VkBot.SessionAuth(1)
    VkBot.GroupAlbumPhoto()
    VkBot.SessionAuth(0)

    for event in VkBot.longpoll.listen():
        # Обработка сообщений пользователей
        if event.type == VkBot.VkBotEventType.MESSAGE_NEW:
            text = event.object['message']['text'].lower()
            if len(event.object['message']['attachments']) != 0:
                if len(event.object['message']['attachments']) == 1:
                    VkBot.UserPhoto(event)
                else:
                    VkBot.vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                            'message': 'Пожалуйста, пришлите одну фотографию',
                                                            'random_id': 0})
            elif text == 'найти фотографии':
                VkBot.vk_session.method('messages.send', {'user_id': event.object['message']['from_id'],
                                                        'message': 'Пожалуйста, пришлите фотографию',
                                                        'random_id': 0})
            elif text == 'закрыть клавиатуру':
                keyboard = VkBot.Create_board(text)
                VkBot.vk_session.method('messages.send', {'user_id': event.object['message']['from_id'], 'message': ':(',
                                                        'random_id': 0, 'keyboard': keyboard})
            elif text != '':
                keyboard = VkBot.Create_board()
                VkBot.vk_session.method('messages.send',
                                      {'user_id': event.object['message']['from_id'], 'message': 'Приветствую!\n'
                                                                                                 '\tОзнакомься со списком команд:\n'
                                                                                                 '\t 1. Найти в сообществе все фотографии со мной\n'
                                                                                                 '\t 2. \n', 'random_id': 0, 'keyboard': keyboard})

        # Сохранение новых фотографий в альбомах сообщества
        if event.type == VkBot.VkBotEventType.PHOTO_NEW:
            VkBot.GroupAlbumPhoto(event)
        # Сохранение фотографий с нового поста сообщества
        if event.type == VkBot.VkBotEventType.WALL_POST_NEW:
            VkBot.GroupWallPhoto(event)
