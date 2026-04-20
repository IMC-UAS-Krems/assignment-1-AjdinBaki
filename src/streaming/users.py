from datetime import date

class User:
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_listening_seconds(self):
        total = 0
        for session in self.sessions:
            total = total + session.duration_listened_seconds
        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self):
        track_ids = set()
        for session in self.sessions:
            track_ids.add(session.track.track_id)
        return track_ids


class FreeUser(User):
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(PremiumUser):
    def __init__(self, user_id: str, name: str, age: int, subscription_start=None):
        super().__init__(user_id, name, age, subscription_start)
        self.sub_users = []

    def add_sub_user(self, user):
        if user not in self.sub_users:
            self.sub_users.append(user)

    def all_members(self):
        return [self] + self.sub_users


class FamilyMember(User):
    def __init__(self, user_id: str, name: str, age: int, parent):
        super().__init__(user_id, name, age)
        self.parent = parent