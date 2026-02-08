def format_time(ms):
    if ms <= 0:
        return "00:00"
    seconds = int(ms / 1000)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"
