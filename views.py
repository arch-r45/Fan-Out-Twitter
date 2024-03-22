""""
Two methods, POST Tweet and get timeline
Follow is another method
Auth(Dummy so we do not need this to be crazy)
User Model {
Username *
Password *
Tweets
Followers
}
POST Request- Create Tweet(Update Status) {
Userid 
Tweet String
}
POST Request {
Follow a User 
}
GET Request {
Get timeline --> 
You need to compile all the users Tweets and sort them by time
}

"""
from fastapi import FastAPI
import sqlite3
app = FastAPI()
con = sqlite3.connect("base.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT, password TEXT)")
con.commit()
class UserModel():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tweets = []
        self.following = []
        self.followers = []

@app.post('/signup')
def register(username:str, password:str):
    user = UserModel(username, password)
    cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (user.username, user.password))
    con.commit()
    return {"status": "Success", "message": "User registered successfully"}



@app.post('/signin')
def signin(username: str, password: str):
    user = UserModel(username, password)
    res = cur.execute("SELECT username, password FROM Users WHERE (username = ? and password = ?)", (user.username, user.password))
    user_record = res.fetchone()
    print(user_record)
    if user_record== None:
        return {"status": "Failure", "message": "User Password Incorrect"} 
    
    else:
        return {"status": "Success",  "message": "User successfully authenticated."}
