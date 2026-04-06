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