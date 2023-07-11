
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

class Video:

    def __init__(self, video_id: str):
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        try:
            self.__video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
            self.title: str = self.__video_response['items'][0]['snippet']['title']
        except IndexError:
            print("Ошибка инициализации, возможно был передан несуществующий id видео")
        else:
            self.url: str = f"https://youtu.be/{self.video_id}"
            self.view_count: int = self.__video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.__video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):


    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

