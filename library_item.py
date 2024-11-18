class LibraryItem:
    def __init__(self, name, artist, rating=0, play_count=0, youtube_link=""):
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = play_count
        self.youtube_link = youtube_link

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"

    def stars(self):
        stars = ""
        for i in range(self.rating):
            stars += "*"
        return stars
