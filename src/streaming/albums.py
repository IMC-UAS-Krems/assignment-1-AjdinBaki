class Album:
    def __init__(self, album_id: str, title: str, artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track):
        track.album = self
        self.tracks.append(track)
        for i in range(len(self.tracks)):
            for j in range(i + 1, len(self.tracks)):
                if self.tracks[i].track_number > self.tracks[j].track_number:
                    temp = self.tracks[i]
                    self.tracks[i] = self.tracks[j]
                    self.tracks[j] = temp

    def track_ids(self):
        ids = set()
        for track in self.tracks:
            ids.add(track.track_id)
        return ids

    def duration_seconds(self):
        total = 0
        for track in self.tracks:
            total = total + track.duration_seconds
        return total