"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
 
    def __init__(self, playlist_id, title, owner):
        self.playlist_id = playlist_id
        self.title = title
        self.owner = owner
        self.tracks = []
 
    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)
 
    def remove_track(self, track_id):
        for track in self.tracks:
            if track.track_id == track_id:
                self.tracks.remove(track)
                return
 
    def total_duration_seconds(self):
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total
 
 
class CollaborativePlaylist(Playlist):
 
    def __init__(self, playlist_id, title, owner):
        super().__init__(playlist_id, title, owner)
        self.contributors = [owner]
 
    def add_contributor(self, user):
        if user not in self.contributors:
            self.contributors.append(user)
 
    def remove_contributor(self, user):
        if user in self.contributors and user != self.owner:
            self.contributors.remove(user)