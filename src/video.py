import json
import os
from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY')
# создаем специальный объект для работы с API
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)


class Video:
	"""Видео"""

	def __init__(self, video_id) -> None:
		try:
			self.video_id = video_id  # id видео
			self.video_response = YOUTUBE.videos().list(part='snippet,statistics', id=video_id).execute()  # получаем данные
			self.json_data = json.dumps(self.video_response, indent=2, ensure_ascii=False)  # сохраняем в файл
			self.title = json.loads(self.json_data)["items"][0]['snippet']['title']  # название видео
			self.url = json.loads(self.json_data)["items"][0]['snippet']['thumbnails']['medium']['url']  # ссылка на видео
			self.count_views = json.loads(self.json_data)["items"][0]['statistics']['viewCount']  # количество просмотров
			self.count_likes = json.loads(self.json_data)["items"][0]['statistics']['likeCount']  # количество лайков

		except(IndexError, KeyError):
			self.title = None
			self.count_likes = None

	def __str__(self):
		return self.title

	def __repr__(self):
		"""Удобный вывод"""
		return f'''
Класс : "{self.__class__.__name__}"
Название видео : {self.title}
Ссылка на видео : {self.url}
Количество просмотров : {self.count_views}
Количество лайков : {self.count_likes}
{50 * '-'}'''


class PLVideo(Video):
	"""Плейлист"""

	def __init__(self, video_id, playlist_id) -> None:
		super().__init__(video_id)
		self.playlist_id = playlist_id

	def __str__(self):
		return self.title

	def __repr__(self):
		"""Удобный вывод"""
		return f'''
Класс : "{self.__class__.__name__}"
Id видео : {self.video_id}
Id плейлиста : {self.playlist_id}
Название видео : {self.title}
Ссылка на видео : {self.url}
Количество просмотров : {self.count_views}
Количество лайков : {self.count_likes}
{50 * '-'}'''
