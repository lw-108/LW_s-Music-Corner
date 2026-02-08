from mutagen import File
import os

def get_metadata(path):
    audio = File(path)
    if audio is None:
        return {
            "title": os.path.basename(path),
            "artist": "Unknown",
            "album": "Unknown"
        }

    title = str(audio.tags.get("TIT2", os.path.basename(path)))
    artist = str(audio.tags.get("TPE1", "Unknown"))
    album = str(audio.tags.get("TALB", "Unknown"))

    return {
        "title": title,
        "artist": artist,
        "album": album
    }
