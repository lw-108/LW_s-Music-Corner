import os
from PyQt6.QtWidgets import (
    QMainWindow, QFileDialog, QListWidget,
    QPushButton, QSlider, QLabel,
    QHBoxLayout, QVBoxLayout, QWidget
)
from PyQt6.QtCore import Qt, QTimer

from core.player import AudioPlayer
from core.playlist import Playlist
from utils.time_format import format_time
from utils.metadata import get_metadata


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Music Player 🎵")
        self.setGeometry(300, 100, 700, 500)

        self.player = AudioPlayer()
        self.playlist = Playlist()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)

        self.setup_ui()

    def setup_ui(self):
        self.playlist_widget = QListWidget()
        self.playlist_widget.doubleClicked.connect(self.play_selected)

        self.open_btn = QPushButton("Open File")
        self.open_btn.clicked.connect(self.open_file)

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_pause)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_music)

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.next_track)

        self.prev_btn = QPushButton("Prev")
        self.prev_btn.clicked.connect(self.prev_track)

        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.sliderMoved.connect(self.seek)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.player.set_volume)

        self.time_label = QLabel("00:00 / 00:00")
        self.meta_label = QLabel("No track loaded")

        controls = QHBoxLayout()
        controls.addWidget(self.prev_btn)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.stop_btn)
        controls.addWidget(self.next_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.open_btn)
        layout.addWidget(self.playlist_widget)
        layout.addLayout(controls)
        layout.addWidget(self.position_slider)
        layout.addWidget(self.time_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.volume_slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open Audio", "", "Audio Files (*.mp3 *.wav)")
        for file in files:
            self.playlist.add(file)
            self.playlist_widget.addItem(os.path.basename(file))

    def play_selected(self):
        index = self.playlist_widget.currentRow()
        self.playlist.set_index(index)
        self.load_and_play()

    def load_and_play(self):
        track = self.playlist.current()
        if track:
            self.player.load(track)
            self.player.play()
            self.timer.start(1000)
            metadata = get_metadata(track)
            self.meta_label.setText(f"{metadata['title']} - {metadata['artist']}")

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_btn.setText("Play")
        else:
            self.player.play()
            self.play_btn.setText("Pause")

    def stop_music(self):
        self.player.stop()
        self.play_btn.setText("Play")

    def next_track(self):
        track = self.playlist.next()
        if track:
            self.load_and_play()

    def prev_track(self):
        track = self.playlist.previous()
        if track:
            self.load_and_play()

    def update_ui(self):
        current = self.player.get_time()
        total = self.player.get_length()

        if total > 0:
            position = current / total
            self.position_slider.setValue(int(position * 100))

        self.time_label.setText(f"{format_time(current)} / {format_time(total)}")

    def seek(self, value):
        self.player.set_position(value / 100)
