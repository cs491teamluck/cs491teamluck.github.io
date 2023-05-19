from userSongsRepository import userSongsRepo

class UserSongsService:
    def __init__(self):
        pass

    def getUserSongs(self , userID):
        if userID != -1:
            return userSongsRepo.getUserSongs(userID)
        else:
            return None
        
userSongsService = UserSongsService()