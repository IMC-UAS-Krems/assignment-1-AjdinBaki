from datetime import datetime, timedelta
from streaming.users import PremiumUser, FamilyMember
from streaming.tracks import Song
from streaming.playlists import CollaborativePlaylist

class StreamingPlatform:
    def __init__(self, name: str):
        self.name = name
        self.catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track):
        self.catalogue[track.track_id] = track

    def total_listening_time_minutes(self, start, end):
        total_seconds = 0
        for session in self._sessions:
            if session.timestamp >= start:
                if session.timestamp <= end:
                    seconds = session.duration_listened_seconds
                    total_seconds = total_seconds + seconds
        minutes = total_seconds / 60.0
        return minutes

    def avg_unique_tracks_per_premium_user(self, days=30):
        premium_users = []
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)
        if len(premium_users) == 0:
            return 0.0
        cutoff_date = datetime.now() - timedelta(days=days)
        total_unique_tracks = 0
        for user in premium_users:
            unique_tracks = set()
            for session in user.sessions:
                if session.timestamp >= cutoff_date:
                    unique_tracks.add(session.track.track_id)
            total_unique_tracks = total_unique_tracks + len(unique_tracks)
        average = total_unique_tracks / len(premium_users)
        return average

    def track_with_most_distinct_listeners(self):
        if len(self._sessions) == 0:
            return None
        track_listeners = {}
        for session in self._sessions:
            track_id = session.track.track_id
            user_id = session.user.user_id
            if track_id not in track_listeners:
                track_listeners[track_id] = set()
            track_listeners[track_id].add(user_id)
        best_track_id = None
        highest_count = 0

        for track_id in track_listeners:
            listener_count = len(track_listeners[track_id])
            if listener_count > highest_count:
                highest_count = listener_count
                best_track_id = track_id
        return self.catalogue[best_track_id]

    def avg_session_duration_by_user_type(self):
        type_totals = {}
        type_counts = {}
        for session in self._sessions:
            user_type = type(session.user).__name__
            if user_type not in type_totals:
                type_totals[user_type] = 0
                type_counts[user_type] = 0
            type_totals[user_type] = type_totals[user_type] + session.duration_listened_seconds
            type_counts[user_type] = type_counts[user_type] +  1
        result = []

        for user_type in type_totals:
            total = type_totals[user_type]
            count = type_counts[user_type]
            average = total / count
            result.append((user_type, average))
        for i in range(len(result)):
            for j in range(i + 1, len(result)):
                if result[i][1] < result[j][1]:
                    temp = result[i]
                    result[i] = result[j]
                    result[j] = temp
        return result

    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total_seconds = 0

        for session in self._sessions:
            user = session.user

            if isinstance(user, FamilyMember):
                if user.age < age_threshold:
                    total_seconds += session.duration_listened_seconds

        minutes = total_seconds / 60.0
        return minutes

    def top_artists_by_listening_time(self, n=5):
        artist_times = {}
        for session in self._sessions:
            track = session.track
            if isinstance(track, Song):
                artist = track.artist
                seconds = session.duration_listened_seconds
                if artist not in artist_times:
                    artist_times[artist] = 0
                artist_times[artist] += seconds
        artist_list = []
        for artist in artist_times:
            total_seconds = artist_times[artist]
            minutes = total_seconds / 60.0
            artist_list.append((artist, minutes))
        for i in range(len(artist_list)):
            for j in range(i + 1, len(artist_list)):
                if artist_list[i][1] < artist_list[j][1]:
                    temp = artist_list[i]
                    artist_list[i] = artist_list[j]
                    artist_list[j] = temp
        return artist_list[:n]

    def user_top_genre(self, user_id):
        user = self.get_user(user_id)
        if user is None:
            return None
        if len(user.sessions) == 0:
            return None
        genre_times = {}
        total_seconds = 0
        for session in user.sessions:
            genre = session.track.genre
            seconds = session.duration_listened_seconds
            if genre not in genre_times:
                genre_times[genre] = 0
            genre_times[genre] = genre_times[genre] + seconds
            total_seconds = total_seconds + seconds
        top_genre = None
        max_seconds = 0
        for genre in genre_times:
            if genre_times[genre] > max_seconds:
                max_seconds = genre_times[genre]
                top_genre = genre
        percentage = (max_seconds / total_seconds) * 100
        return (top_genre, percentage)
    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists = set()
                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists.add(track.artist)
                if len(artists) > threshold:
                    result.append(playlist)
        return result

    def avg_tracks_per_playlist_type(self):
        playlist_total = 0
        playlist_count = 0
        collab_total = 0
        collab_count = 0
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collab_total += len(playlist.tracks)
                collab_count += 1
            else:
                playlist_total += len(playlist.tracks)
                playlist_count += 1
        if playlist_count == 0:
            avg_playlist = 0.0
        else:
            avg_playlist = playlist_total / playlist_count
        if collab_count == 0:
            avg_collab = 0.0
        else:
            avg_collab = collab_total / collab_count
        result = {
            "Playlist": avg_playlist,
            "CollaborativePlaylist": avg_collab
        }
        return result

    def users_who_completed_albums(self):
        result = []
        for user in self._users.values():
            completed_albums = []
            listened_tracks = set()
            for session in user.sessions:
                listened_tracks.add(session.track.track_id)
            for album in self._albums.values():
                if len(album.tracks) == 0:
                    continue
                all_tracks_in_album = True
                for track in album.tracks:
                    if track.track_id not in listened_tracks:
                        all_tracks_in_album = False
                if all_tracks_in_album:
                    completed_albums.append(album.title)
            if len(completed_albums) > 0:
                result.append((user, completed_albums))
        return result

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        session.user.sessions.append(session)

    def get_track(self, track_id):
        return self.catalogue.get(track_id)

    def get_user(self, user_id):
        return self._users.get(user_id)

    def get_artist(self, artist_id):
        return self._artists.get(artist_id)

    def get_album(self, album_id):
        return self._albums.get(album_id)

    def all_users(self):
        return list(self._users.values())

    def all_tracks(self):
        return list(self.catalogue.values())