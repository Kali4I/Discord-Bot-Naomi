# coding: utf-8

import discord
import asyncio
import json
import os
import io

bot_config = {
    'cmd-prefix': 'n!',
    'mute-role': 'mute',
    'max-warns': 10,
    'admins': []
}

user_info = {
    'is_muted': False,
    'warn_count': 0,
    'level': 0
}

card_info = {
    'status': None,
    'description': None,
    'banner': None,
    'vk': None,
    'google': None,
    'instagram': None,
    'facebook': None,
    'twitter': None
}
class Data:
    '''Загрузка ресурсов из сохраненных файлов.'''

    class card:
        '''Загрузка информации о пользователе из его личной карточки / ее создание.'''
        @classmethod
        def load(self, user: discord.User):
            '''Получить информацию из файла.'''
            try: card = json.load(io.open(f'rewrite_res/cards/{user.id}.json', 'r', encoding='utf-8-sig'))
            except:
                if not os.path.exists('rewrite_res/cards'):
                    os.makedirs('rewrite_res/cards')

                json.dump(card_info, io.open(f'rewrite_res/cards/{user.id}.json', 'w', encoding='utf-8-sig'), indent=4)
                new_card = card_info
                new_card['description'] = 'Ничего интересного.'
                new_card['status'] = 'Пусто'
                return new_card
            else:
                return card

        @classmethod
        def upload(self, user: discord.User, content: dict):
            '''Записать информацию в файл.'''
            try: json.dump(content, io.open(f'rewrite_res/cards/{user.id}.json', 'w', encoding='utf-8-sig'), indent=4)
            except:
                return False
            else:
                return True
    class user:
        '''Загрузка статистики пользователя (варны, мут).'''
        @classmethod
        def load(self, user, guild: discord.Guild):
            '''Получить информацию из файла.'''
            try: user = json.load(io.open(f'rewrite_res/users/{guild.id}/{user.id}.json', 'r', encoding='utf-8-sig'))
            except:
                if not os.path.exists(f'rewrite_res/users/{guild.id}'):
                    os.makedirs(f'rewrite_res/users/{guild.id}')

                json.dump(user_info, io.open(f'rewrite_res/users/{guild.id}/{user.id}.json', 'w', encoding='utf-8-sig'), indent=4)
                return user_info
            else:
                return user

        @classmethod
        def get(self, user: str, guild: discord.Guild):
            '''Получить discord.User из str.'''
            _user = str(user).replace('<', '').replace('>', '').replace('@', '').replace('!', '').replace('&', '')
            if _user.isnumeric():
                return self.guild.get_member(_user)
            else:
                return discord.utils.get(guild.members, name=_user)

        @classmethod
        def upload(self, user: discord.User, guild: discord.Guild, content: dict):
            '''Записать информацию в файл.'''
            try: json.dump(content, io.open(f'rewrite_res/users/{guild.id}/{user.id}.json', 'w', encoding='utf-8-sig'), indent=4)
            except:
                return False
            else:
                return True

    class config:
        '''Загрузка конфигурации бота для определенного сервера.'''
        @classmethod
        def load(self, guild: discord.Guild):
            '''Получить информацию из файла.'''
            try:
                bcfg = json.load(io.open(f'rewrite_res/config/{guild.id}.json', 'r', encoding='utf-8-sig'))
                for x in bot_config:
                    for i in bcfg:
                        try: bcfg[f'{x}']
                        except Exception as e:
                            warn(f'KeyError {e} when loading config for {guild.id}.')
                            bcfg[f'{i}'] = bot_config[f'{i}']
                            json.dump(bot_config, io.open(f'rewrite_res/config/{guild.id}.json', 'w', encoding='utf-8-sig'), indent=4)
            except:
                if not os.path.exists('rewrite_res/config'):
                    os.makedirs('rewrite_res/config')

                json.dump(bot_config, io.open(f'rewrite_res/config/{guild.id}.json', 'w', encoding='utf-8-sig'), indent=4)
                return bot_config
            else:
                return bcfg

        @classmethod
        def upload(self, guild: discord.Guild, content: dict):
            '''Записать информацию в файл.'''
            try: json.dump(content, io.open(f'rewrite_res/config/{guild.id}.json', 'w', encoding='utf-8-sig'), indent=4)
            except:
                return False
            else:
                return True

def log(message: str = ''):
    return print(f'[LOG] {message}')

def warn(message: str = ''):
    return print(f'[WARN] {message}')

def error(message: str = ''):
    return print(f'[ERROR] {message}')