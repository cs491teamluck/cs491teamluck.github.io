import glob

class UserSongsRepository:
    def __init__(self):
        pass

    def getUserSongs(self , userID):
        usersongs = []
        for item in glob.glob("static/usersongs/*_" + str(userID) + ".mid"):
            x = item.split('\\')
            usersongs.append(x[1])
        return usersongs
    
userSongsRepo = UserSongsRepository()