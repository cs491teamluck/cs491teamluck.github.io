from songsRepository import songsRepo

class SongsService:
    def __init__(self):
        pass

    def getCreationSongs(self):
        return songsRepo.getSongs()
    
songsService = SongsService()