
import os
import isodate
import datetime

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YT_API_KEY')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.__playlist = youtube.playlists().list(id=self.playlist_id,
                                                       part='snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.title: str = self.__playlist['items'][0]['snippet']['title']
        self.url: str = f"https://www.youtube.com/playlist?list={self.playlist_id}"


    def video_response(self):
        """
        возвращает словарь с информацией по видеороликам из плейлиста
        """
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response


    @property
    def total_duration(self):
        """
        возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        """
        duration_sum = datetime.timedelta(0)
        for video in self.video_response()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_sum += duration
        return duration_sum


    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        best_video_like_count = 0
        best_video_url = None
        for video in self.video_response()['items']:
            if int(video['statistics']['likeCount']) > best_video_like_count:
                best_video_like_count = int(video['statistics']['likeCount'])
                best_video_url = f"https://youtu.be/{video['id']}"
        return best_video_url
