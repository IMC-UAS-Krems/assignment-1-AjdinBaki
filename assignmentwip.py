
class artist:
    def __init__(self, artst_id, genre, name, tracks):
        self.arist_id = artist_id
        self.genre = genre
        self.name = name
        self.tracks = tracks
class album:
    def __init__(self, album_id, title,artist,release_year,tracks):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks
class listeningsession:
    def __init__(self, session_id,user,track,datetime,duration_listened_seconds):
        self.session_id = session_id
        self.user = user
        self.track = track
        self.datetime = datetime
        self.duration_listened_seconds = duration_listened_seconds
class playlist:
    def __init__(self, playlist_id, name, owner, tracks):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks

class track:
    def __init__(self, artist):
class freeuser:
    def __init__(self, user_id, name, age, sessions, max_skips_per_hour):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions
        self.max_skips_per_hour = max_skips_per_hour

class premiumuser:
    def __init__(self, user_id, name, age, sessions, subscription_start):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions
        self.subscription_start = subscription_start

class familyaccountuser:
    def __init__(self, user_id, name, age, sessions, sub_users):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions
        self.sub_users = sub_users

class familymember:
    def __init__(self, user_id, name, age, sessions, parent):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = sessions
        self.parent = parent

class streamingplatform:
    def __init__(self, name, catalogue, users, artists, albums, playlists, sessions):
        self.name = name
        self.catalogue = catalogue
        self.users = users
        self.artists = artists
        self.albums = albums
        self.playlists = playlists
        self.sessions = sessions