"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
 
from streaming.tracks import Song
from streaming.users import PremiumUser, FamilyMember
from streaming.playlists import CollaborativePlaylist
 
 
class StreamingPlatform:
 
    def __init__(self, name):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []
 
    # Registration methods
 
    def add_track(self, track):
        self._catalogue[track.track_id] = track
 
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
        session.user.add_session(session)
 
    # Accessors
 
    def get_track(self, track_id):
        return self._catalogue.get(track_id)
 
    def get_user(self, user_id):
        return self._users.get(user_id)
 
    def get_artist(self, artist_id):
        return self._artists.get(artist_id)
 
    def get_album(self, album_id):
        return self._albums.get(album_id)
 
    def all_users(self):
        return list(self._users.values())
 
    def all_tracks(self):
        return list(self._catalogue.values())
 
    # Q1: Total cumulative listening time for a given period
 
    def total_listening_time_minutes(self, start, end):
        total = 0
        for session in self._sessions:
            if start <= session.timestamp <= end:
                total += session.duration_listened_seconds
        return total / 60.0
 
    # Q2: Average unique tracks per PremiumUser in the last N days
 
    def avg_unique_tracks_per_premium_user(self, days=30):
        cutoff = datetime.now() - timedelta(days=days)
 
        premium_users = []
        for user in self._users.values():
            if type(user) is PremiumUser:
                premium_users.append(user)
 
        if len(premium_users) == 0:
            return 0.0
 
        total_unique = 0
        for user in premium_users:
            unique = set()
            for s in user.sessions:
                if s.timestamp >= cutoff:
                    unique.add(s.track.track_id)
            total_unique += len(unique)
 
        return total_unique / len(premium_users)
 
    # Q3: Track with the most distinct listeners
 
    def track_with_most_distinct_listeners(self):
        if len(self._sessions) == 0:
            return None
 
        listeners = {}
        for session in self._sessions:
            tid = session.track.track_id
            if tid not in listeners:
                listeners[tid] = set()
            listeners[tid].add(session.user.user_id)
 
        best_id = None
        best_count = 0
        for tid, users in listeners.items():
            if len(users) > best_count:
                best_count = len(users)
                best_id = tid
 
        return self._catalogue.get(best_id)
 
    # Q4: Average session duration by user type, ranked descending
 
    def avg_session_duration_by_user_type(self):
        totals = {}
 
        for session in self._sessions:
            type_name = type(session.user).__name__
            if type_name not in totals:
                totals[type_name] = []
            totals[type_name].append(session.duration_listened_seconds)
 
        result = []
        for type_name, durations in totals.items():
            avg = sum(durations) / len(durations)
            result.append((type_name, float(avg)))
 
        result.sort(key=lambda x: x[1], reverse=True)
        return result
 
    # Q5: Total listening time for underage FamilyMember sub-users
 
    def total_listening_time_underage_sub_users_minutes(self, age_threshold=18):
        total = 0
        for session in self._sessions:
            user = session.user
            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total += session.duration_listened_seconds
        return total / 60.0
 
    # Q6: Top N artists by total listening time (Songs only)
 
    def top_artists_by_listening_time(self, n=5):
        totals = {}
 
        for session in self._sessions:
            track = session.track
            if isinstance(track, Song):
                aid = track.artist.artist_id
                if aid not in totals:
                    totals[aid] = 0
                totals[aid] += session.duration_listened_seconds
 
        result = []
        for aid, seconds in totals.items():
            if aid in self._artists:
                result.append((self._artists[aid], seconds / 60.0))
 
        result.sort(key=lambda x: x[1], reverse=True)
        return result[:n]
 
    # Q7: User's top genre and percentage of total listening time
 
    def user_top_genre(self, user_id):
        user = self._users.get(user_id)
        if user is None or len(user.sessions) == 0:
            return None
 
        genre_seconds = {}
        for session in user.sessions:
            genre = session.track.genre
            if genre not in genre_seconds:
                genre_seconds[genre] = 0
            genre_seconds[genre] += session.duration_listened_seconds
 
        top_genre = None
        top_seconds = 0
        for genre, seconds in genre_seconds.items():
            if seconds > top_seconds:
                top_seconds = seconds
                top_genre = genre
 
        total = sum(genre_seconds.values())
        percentage = (top_seconds / total) * 100.0
        return (top_genre, percentage)
 
    # Q8: CollaborativePlaylists with more than threshold distinct artists
 
    def collaborative_playlists_with_many_artists(self, threshold=3):
        result = []
        for playlist in self._playlists.values():
            if not isinstance(playlist, CollaborativePlaylist):
                continue
            artists = set()
            for track in playlist.tracks:
                if isinstance(track, Song):
                    artists.add(track.artist.artist_id)
            if len(artists) > threshold:
                result.append(playlist)
        return result
 
    # Q9: Average tracks per playlist type
 
    def avg_tracks_per_playlist_type(self):
        standard = []
        collaborative = []
 
        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                collaborative.append(playlist)
            else:
                standard.append(playlist)
 
        if len(standard) > 0:
            avg_standard = sum(len(p.tracks) for p in standard) / len(standard)
        else:
            avg_standard = 0.0
 
        if len(collaborative) > 0:
            avg_collab = sum(len(p.tracks) for p in collaborative) / len(collaborative)
        else:
            avg_collab = 0.0
 
        return {"Playlist": avg_standard, "CollaborativePlaylist": avg_collab}
 
    # Q10: Users who listened to every track on at least one album
 
    def users_who_completed_albums(self):
        result = []
        for user in self._users.values():
            listened = set()
            for s in user.sessions:
                listened.add(s.track.track_id)
 
            completed_titles = []
            for album in self._albums.values():
                if len(album.tracks) == 0:
                    continue
                all_listened = True
                for track_id in album.track_ids():
                    if track_id not in listened:
                        all_listened = False
                        break
                if all_listened:
                    completed_titles.append(album.title)
 
            if len(completed_titles) > 0:
                result.append((user, completed_titles))
 
        return result