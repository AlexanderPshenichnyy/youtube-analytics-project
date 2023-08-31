import os
import json
from googleapiclient.discovery import build


class Channel:
	"""Класс для ютуб-канала"""
	api_key: str = os.getenv('API_KEY')
	# создаем специальный объект для работы с API
	youtube = build('youtube', 'v3', developerKey=api_key)

	def __init__(self, channel_id: str) -> None:
		"""Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

		# id канала
		self.__channel_id = channel_id

		# получаем данные канала
		self.channel_data = self.get_service().channels().list(id=self.__channel_id,
															   part='snippet,statistics').execute()

		# сохраняем в файл
		self.json_data = json.dumps(self.channel_data, indent=2, ensure_ascii=False)

		# название канала
		self.title = json.loads(self.json_data)["items"][0]['snippet']['title']

		# описание канала
		self.description = json.loads(self.json_data)["items"][0]['snippet']['description']

		# ссылка на канал
		self.url = f"{'https://www.youtube.com/channel/'}{channel_id}"

		# количество подписчиков
		self.count_subscribers = json.loads(self.json_data)["items"][0]["statistics"]["subscriberCount"]

		# количество видео
		self.count_videos = json.loads(self.json_data)["items"][0]["statistics"]["videoCount"]

		# общее количество просмотров
		self.count_views = json.loads(self.json_data)["items"][0]["statistics"]["viewCount"]

	def __str__(self):
		"""Возвращает название канала"""
		return f'{self.title} ({self.url})'

	def __add__(self, other):
		"""Сложение каналов"""
		return int(self.count_subscribers) + int(other.count_subscribers)

	def __sub__(self, other):
		"""Вычитание каналов"""
		return int(self.count_subscribers) - int(other.count_subscribers)

	def __rsub__(self, other):
		"""Вычитание каналов"""
		return other.count_subscribers - self.count_subscribers

	def __gt__(self, other):
		"""Сравнение каналов"""
		return self.count_subscribers > other.count_subscribers

	def __ge__(self, other):
		"""Сравнение каналов"""
		return self.count_subscribers >= other.count_subscribers

	def __lt__(self, other):
		"""Сравнение каналов"""
		return self.count_subscribers < other.count_subscribers

	def __le__(self, other):
		"""Сравнение каналов"""
		return self.count_subscribers <= other.count_subscribers

	def print_info(self):
		"""Выводит в консоль информацию о канале."""

		channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

		print(json.dumps(channel, indent=2, ensure_ascii=False))

	@classmethod
	def get_service(cls):
		"""Возвращает объект для работы с API"""
		return cls.youtube

	def to_json(self, name_file_json: str):
		"""Сохраняет данные канала в файл"""
		with open(name_file_json, "a", encoding='UTF-8') as file:
			json.dump(self.channel_data, file)

	@property
	def channel_id(self):
		"""Возвращает id канала"""
		return self.__channel_id
