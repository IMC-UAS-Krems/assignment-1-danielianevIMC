"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from datetime import date
 
 
class User:
 
    def __init__(self, user_id, name, age):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []
 
    def add_session(self, session):
        self.sessions.append(session)
 
    def total_listening_seconds(self):
        total = 0
        for s in self.sessions:
            total += s.duration_listened_seconds
        return total
 
    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60.0
 
    def unique_tracks_listened(self):
        track_ids = set()
        for s in self.sessions:
            track_ids.add(s.track.track_id)
        return track_ids
 
 
class FreeUser(User):
 
    MAX_SKIPS_PER_HOUR = 6
 
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
 
 
class PremiumUser(User):
 
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start
 
 
class FamilyAccountUser(PremiumUser):
 
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age, subscription_start=date.today())
        self.sub_users = []
 
    def add_sub_user(self, sub_user):
        if sub_user not in self.sub_users:
            self.sub_users.append(sub_user)
 
    def all_members(self):
        return [self] + list(self.sub_users)
 
 
class FamilyMember(User):
 
    def __init__(self, user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent