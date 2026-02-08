import vlc

class AudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def load(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.is_playing()

    def set_volume(self, value):
        self.player.audio_set_volume(value)

    def get_time(self):
        return self.player.get_time()

    def get_length(self):
        return self.player.get_length()

    def set_position(self, pos):
        self.player.set_position(pos)
