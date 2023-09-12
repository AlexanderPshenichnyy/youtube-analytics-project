import isodate
import datetime
from src.channel import Channel


class PlayList(Channel):
	""" Класс для работы с плейлистами """
	def __init__(self, playlist_id: str):
		self.playlist_id = playlist_id
		self.playlists = self.get_service().playlists().list(
			id=playlist_id,
			part='snippet'
		).execute()
		self.title = self.playlists['items'][0]['snippet']['title']
		self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
		self.playlist_videos = self.get_service().playlistItems().list(
			playlistId=playlist_id,
			part='contentDetails',
			maxResults=50
		).execute()

		# список всех id видеороликов из плейлиста
		video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

		# данные видеороликов по их id из плейлиста
		self.video_response = self.get_service().videos().list(
			part='contentDetails,statistics',
			id=','.join(video_ids)
		).execute()

	@property
	def total_duration(self) -> datetime.timedelta:

		"""
		Переводит продолжительность видео из формата ISO 8601 в объект класса `datetime.timedelta`
		и возвращает суммарную длительность плейлиста в виде объекта класса `datetime.timedelta`
		"""
		total_duration = datetime.timedelta()
		for video in self.video_response['items']:
			# YouTube video duration is in ISO 8601 format
			iso_8601_duration = video['contentDetails']['duration']
			duration = isodate.parse_duration(iso_8601_duration)
			total_duration += duration
		return total_duration

	def show_best_video(self) -> str:
		"""Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
		most_liked = 0
		video_id = ''
		for video in self.video_response['items']:
			likes_count = int(video['statistics']['likeCount'])
			if most_liked < likes_count:
				most_liked = likes_count
				video_id = video['id']
		return f'https://youtu.be/{video_id}'
