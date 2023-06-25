
import os
import json

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Инициализация экземпляра класса по id канала,
        инициализация атрибутов экземпляра класса"""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id,
                                          part='snippet,statistics').execute()
        self.title: str = self.channel["items"][0]["snippet"]["title"]
        self.description: str = self.channel["items"][0]["snippet"]["description"]
        self.url: str = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count: int = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count: int = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count: int = self.channel["items"][0]["statistics"]["viewCount"]


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id,
        part='snippet,statistics').execute()
        return print(channel)


    @classmethod
    def get_service(cls):
        """
        возвращает объект для работы с YouTube API
        """
        return youtube


    def to_json(self, file):
        """
        создаеn файл 'moscowpython.json' c данными по каналу
        """
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.channel, f)