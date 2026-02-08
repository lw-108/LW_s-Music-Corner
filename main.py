import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QFileDialog,
    QSlider, QListWidget
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from mutagen import File
import qtawesome as qta


SUPPORTED_FORMATS = (
    ".mp3", ".wav", ".ogg", ".flac",
    ".m4a", ".aac", ".wma", ".aiff"
)


class RedOrangePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LW's Music Corner🔥")
        self.resize(1000, 650)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        self.songs = []
        self.current_index = 0

        self.init_ui()
        self.load_local_songs()

    # ================= UI ================= #

    def init_ui(self):

        self.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: white;
        }

        QPushButton {
            background-color: #1f1f1f;
            border-radius: 10px;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #ffffff;
            color: #ff5722;
        }

        QListWidget {
            background-color: #1a1a1a;
            border-radius: 12px;
            padding: 5px;
        }

        QListWidget::item:selected {
            background-color: #ff5722;
        }
        """)

        main_layout = QHBoxLayout(self)

        # ===== LEFT PANEL =====
        left_layout = QVBoxLayout()

        self.cover = QLabel("No Cover")
        self.cover.setMinimumSize(350, 350)
        self.cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover.setStyleSheet("""
            background-color: #1a1a1a;
            border-radius: 20px;
        """)
        left_layout.addWidget(self.cover)

        self.title = QLabel("No Song")
        self.title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.title.setStyleSheet("color:#ff7043;")
        left_layout.addWidget(self.title)

        self.meta = QLabel("")
        self.meta.setStyleSheet("color:#ffab91;")
        left_layout.addWidget(self.meta)

        # ===== Seek Bar =====
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.player.setPosition)
        self.slider.setStyleSheet("""
        QSlider::groove:horizontal {
            height:6px;
            background:#333;
        }

        QSlider::sub-page:horizontal {
            background:#ff5722;
        }

        QSlider::handle:horizontal {
            background:#ff7043;
            width:16px;
            height:16px;
            margin:-5px 0;
            border-radius:8px;
        }
        """)
        left_layout.addWidget(self.slider)

        # ===== Time =====
        time_row = QHBoxLayout()
        self.current_time = QLabel("00:00")
        self.total_time = QLabel("00:00")
        self.current_time.setStyleSheet("color:#ff7043;")
        self.total_time.setStyleSheet("color:#ff7043;")
        time_row.addWidget(self.current_time)
        time_row.addStretch()
        time_row.addWidget(self.total_time)
        left_layout.addLayout(time_row)

        # ===== Controls =====
        controls = QHBoxLayout()

        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(qta.icon('fa5s.backward', color='#ff7043'))
        self.prev_btn.clicked.connect(self.prev_song)

        self.play_btn = QPushButton()
        self.play_btn.setIcon(qta.icon('fa5s.play', color='#ff7043'))
        self.play_btn.clicked.connect(self.play_pause)

        self.next_btn = QPushButton()
        self.next_btn.setIcon(qta.icon('fa5s.forward', color='#ff7043'))
        self.next_btn.clicked.connect(self.next_song)

        controls.addWidget(self.prev_btn)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.next_btn)

        left_layout.addLayout(controls)

        # ===== Volume =====
        volume_row = QHBoxLayout()
        vol_icon = QLabel()
        vol_icon.setPixmap(qta.icon('fa5s.volume-up', color='#ff7043').pixmap(18,18))

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0,100)
        self.volume_slider.setValue(70)
        self.audio_output.setVolume(0.7)
        self.volume_slider.valueChanged.connect(
            lambda v: self.audio_output.setVolume(v/100)
        )

        volume_row.addWidget(vol_icon)
        volume_row.addWidget(self.volume_slider)
        left_layout.addLayout(volume_row)

        # ===== RIGHT PANEL =====
        right_layout = QVBoxLayout()

        self.open_btn = QPushButton("Open File")
        self.open_btn.setIcon(qta.icon('fa5s.folder-open', color='#ff7043'))
        self.open_btn.clicked.connect(self.open_file)
        right_layout.addWidget(self.open_btn)

        self.playlist = QListWidget()
        self.playlist.clicked.connect(self.play_selected)
        right_layout.addWidget(self.playlist)

        main_layout.addLayout(left_layout, 2)
        main_layout.addLayout(right_layout, 1)

    # ================= Logic ================= #

    def load_local_songs(self):
        folder = "songs"
        os.makedirs(folder, exist_ok=True)
        for file in os.listdir(folder):
            if file.lower().endswith(SUPPORTED_FORMATS):
                full = os.path.join(folder, file)
                self.songs.append(full)
                self.playlist.addItem(file)

    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Open Audio", "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a *.aac *.wma *.aiff)"
        )
        if file:
            self.songs.append(file)
            self.playlist.addItem(os.path.basename(file))

    def play_selected(self):
        self.current_index = self.playlist.currentRow()
        self.play_song()

    def play_song(self):
        if not self.songs:
            return
        file = self.songs[self.current_index]
        self.player.setSource(QUrl.fromLocalFile(file))
        self.load_metadata(file)
        self.player.play()
        self.play_btn.setIcon(qta.icon('fa5s.pause', color='#ff7043'))

    def play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_btn.setIcon(qta.icon('fa5s.play', color='#ff7043'))
        else:
            self.player.play()
            self.play_btn.setIcon(qta.icon('fa5s.pause', color='#ff7043'))

    def next_song(self):
        self.current_index = (self.current_index+1)%len(self.songs)
        self.play_song()

    def prev_song(self):
        self.current_index = (self.current_index-1)%len(self.songs)
        self.play_song()

    def load_metadata(self, file):
        audio = File(file)
        title = os.path.basename(file)
        artist = ""

        if audio and audio.tags:
            tags = audio.tags
            if "TIT2" in tags: title = str(tags["TIT2"])
            if "TPE1" in tags: artist = str(tags["TPE1"])

            for tag in tags.values():
                if hasattr(tag, "data"):
                    pix = QPixmap()
                    pix.loadFromData(tag.data)
                    pix = pix.scaled(
                        400,400,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.cover.setPixmap(pix)
                    break

        self.title.setText(title)
        self.meta.setText(artist)

    def update_position(self, pos):
        self.slider.setValue(pos)
        self.current_time.setText(self.format_time(pos))

    def update_duration(self, dur):
        self.slider.setRange(0, dur)
        self.total_time.setText(self.format_time(dur))

    def format_time(self, ms):
        s = ms//1000
        return f"{s//60:02}:{s%60:02}"
        def update_position(self, pos):
            self.slider.setValue(pos)
            self.current_time.setText(self.format_time(pos))

        def update_duration(self, dur):
            self.slider.setRange(0, dur)
            self.total_time.setText(self.format_time(dur))

        def format_time(self, ms):
            s = ms//1000
            return f"{s//60:02}:{s%60:02}"

        def init_buttons_hover(self):
            for btn in [self.prev_btn, self.play_btn, self.next_btn, self.open_btn]:
                btn.enterEvent = lambda e, b=btn: b.setIcon(qta.icon(self.get_icon_name(b), color='black'))
                btn.leaveEvent = lambda e, b=btn: b.setIcon(qta.icon(self.get_icon_name(b), color='#ff7043'))

        def get_icon_name(self, btn):
            icon_map = {
                self.prev_btn: 'fa5s.backward',
                self.play_btn: 'fa5s.play' if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState else 'fa5s.pause',
                self.next_btn: 'fa5s.forward',
                self.open_btn: 'fa5s.folder-open'
            }
            return icon_map.get(btn, 'fa5s.play')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RedOrangePlayer()
    window.show()
    sys.exit(app.exec())
