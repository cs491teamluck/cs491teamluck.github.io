from userService import userService
from userSongsService import userSongsService
from songsService import songsService
from createSong import createSong

class MasterController:
    def __init__(self):
        self.currentUserID = -1
    
    def signup(self , email , password1 , password2):
        return userService.signup(email , password1 , password2)
    
    def login(self , email , password):
        userID , isSuccessful = userService.login(email , password)
        self.currentUserID = int(userID)
        return isSuccessful
    
    def getUserSongs(self , userID):
        return userSongsService.getUserSongs(userID)
    
    def getCreationSongs(self):
        return songsService.getCreationSongs()

    def createSong(self , songName , songLength , generateSongName , userID):
        return createSong(songName , songLength , generateSongName , userID)
    
    def getCurrentUserID(self):
        return self.currentUserID
    
    def setCurrentUserID(self , id):
        self.currentUserID = id

controller = MasterController()