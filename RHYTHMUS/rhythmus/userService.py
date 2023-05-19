from userRepository import userRepo

class UserService:
    def __init__(self):
        pass

    def signup(self , email , password1 , password2):
        if password1 == password2:
            isSuccessful = userRepo.addUser(email , password1)
            return isSuccessful
        else:
            return False
        
    def login(self , email , password):
        userID , userPassword = userRepo.getUser(email)
        
        if  password == userPassword:
            return userID , True
        else:
            return -1 , False
        
userService = UserService() 