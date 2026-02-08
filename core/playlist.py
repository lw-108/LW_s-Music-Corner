class Playlist:
    def __init__(self):
        self.tracks = []
        self.current_index = -1

    def add(self, file):
        self.tracks.append(file)

    def get_all(self):
        return self.tracks

    def next(self):
        if not self.tracks:
            return None
        self.current_index = (self.current_index + 1) % len(self.tracks)
        return self.tracks[self.current_index]

    def previous(self):
        if not self.tracks:
            return None
        self.current_index = (self.current_index - 1) % len(self.tracks)
        return self.tracks[self.current_index]

    def set_index(self, index):
        self.current_index = index

    def current(self):
        if 0 <= self.current_index < len(self.tracks):
            return self.tracks[self.current_index]
        return None
