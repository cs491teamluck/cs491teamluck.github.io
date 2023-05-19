import requests
import json
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.url = 'http://127.0.0.1:8000/rythm/'  
        self.headers = {'Content-Type': 'application/json'}

    def addUser(self , email , password):
        currentDate = datetime.now()
        timestamp = int(round(currentDate.timestamp()))
        
        data = {
            "userid": str(timestamp),
            "email": str(email),
            "password": str(password)
        }

        jsonURL = self.url + "signup/"

        response = requests.post(jsonURL, data=json.dumps(data), headers=self.headers)

        if response.status_code == 200:
            return True
        else:
            return False

    # Return user_id , user_password
    def getUser(self , email):
        jsonURL = self.url + "seeUser/"

        response = requests.get(jsonURL)

        if response.status_code == 200:
            data = response.json()
            for user in data:
                if email == user['email']:
                    uID = user['userid']
                    password = user['password']
                    return int(uID) , password
        else:
            return -1 , None
        
userRepo = UserRepository()