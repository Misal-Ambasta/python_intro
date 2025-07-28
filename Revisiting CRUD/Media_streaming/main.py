from abc import ABC, abstractmethod
from statistics import mean


class MediaContent(ABC):

    def __init__(self, title, premium=False):
        self.title = title
        self.rating = []
        self.premium = premium
    
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def get_duration(self):
        pass

    @abstractmethod
    def get_file_size(self):
        pass

    @abstractmethod
    def calculate_streaming_cost(self):
        pass

    def add_rating(self, rating):
        self.rating.append(rating)

    def get_average_rating(self):
        return mean(self.rating) if self.rating else 0

    def is_premium_content(self):
        return self.premium


class StreamingDevice(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def stream_content(self, content: MediaContent):
        pass

    @abstractmethod
    def adjust_quality(self):
        pass

    def get_device_info(self):
        return f"Device: {self.name}"

    def check_compatibility(self, content: MediaContent):
        return True


class Movie(MediaContent):
    def __init__(self, title, duration, resolution, genre, director, premium=False):
        super().__init__(title, premium)
        self.duration = duration
        self.resolution = resolution
        self.genre = genre
        self.director = director

    def play(self):
        return f"Playing movie: {self.title} in {self.resolution}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 5

    def calculate_streaming_cost(self):
        return 2.5 if self.premium else 1.0


class TVShow(MediaContent):
    def __init__(self, seasons, episodes, current_episode, title, premium=False):
        super().__init__(title, premium)
        self.seasons = seasons
        self.episodes = episodes
        self.current_episode = current_episode

    def play(self):
        return f"Playing TV Show: {self.title}, Episode: {self.current_episode}"

    def get_duration(self):
        return 45  # average episode duration

    def get_file_size(self):
        return self.episodes * 4

    def calculate_streaming_cost(self):
        return 3.0 if self.premium else 1.5


class Podcast(MediaContent):
    def __init__(self, title, episode_number, transcript_available, duration, premium=False):
        super().__init__(title, premium)
        self.episode_number = episode_number
        self.transcript_available = transcript_available
        self.duration = duration

    def play(self):
        return f"Streaming Podcast: {self.title}, Episode: {self.episode_number}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 1

    def calculate_streaming_cost(self):
        return 0.5 if self.premium else 0.2


class Music(MediaContent):
    def __init__(self, title, artist, album, lyrics_available, duration, premium=False):
        super().__init__(title, premium)
        self.artist = artist
        self.album = album
        self.lyrics_available = lyrics_available
        self.duration = duration

    def play(self):
        return f"Playing song: {self.title} by {self.artist}"

    def get_duration(self):
        return self.duration

    def get_file_size(self):
        return self.duration * 0.8

    def calculate_streaming_cost(self):
        return 0.3 if self.premium else 0.1



class SmartTV(StreamingDevice):
    def connect(self):
        return f"{self.name} connected via HDMI"

    def stream_content(self, content: MediaContent):
        return f"{self.name} streaming in 4K: {content.play()}"

    def adjust_quality(self):
        return "Auto-adjusting to 4K resolution"

class Laptop(StreamingDevice):
    def connect(self):
        return f"{self.name} connected to WiFi"

    def stream_content(self, content: MediaContent):
        return f"{self.name} streaming: {content.play()}"

    def adjust_quality(self):
        return "Adjusting to HD resolution"


class Mobile(StreamingDevice):
    def connect(self):
        return f"{self.name} connected via mobile data"

    def stream_content(self, content: MediaContent):
        return f"{self.name} streaming with battery saver: {content.play()}"

    def adjust_quality(self):
        return "Lowering quality to save battery"


class SmartSpeaker(StreamingDevice):
    def connect(self):
        return f"{self.name} connected via voice command"

    def stream_content(self, content: MediaContent):
        return f"{self.name} playing audio: {content.play()}"

    def adjust_quality(self):
        return "Optimizing audio quality"


class User:
    def __init__(self, name, is_premium=False):
        self.name = name
        self.is_premium = is_premium
        self.watch_history = []
        self.preferences  = []

    def play_content(self, content:MediaContent, device: StreamingDevice):
        if content.is_premium_content() and not self.is_premium:
            return f"Upgrade to premium to play {content.title}"
        self.watch_history.append(content.title)
        return device.stream_content(content)

    def recommend(self, contents: list):
        return sorted(contents, key=lambda c: c.get_average_rating(), reverse=True)


class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.contents = []

    def register_user(self, user: User):
        self.users.append(user)

    def upload_content(self, content: MediaContent):
        self.contents.append(content)

    def get_top_content(self, limit=3):
        return sorted(self.contents, key=lambda c: c.get_average_rating(), reverse=True)[:limit]

    def show_catalog(self):
        return [content.title for content in self.contents]

    