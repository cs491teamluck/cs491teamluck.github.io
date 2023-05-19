import glob

class SongsRepository:
    def __init__(self):
        pass

    def getSongs(self):
        songs = []
        for item in glob.glob("static/trainMusics/*.mid"):
            x = item.split('\\')
            songs.append(x[1])
        return songs
    
songsRepo = SongsRepository()