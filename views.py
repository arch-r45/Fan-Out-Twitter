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
    "Check if Username Already Exists"
    user = UserModel(username, password)
    cur.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (user.username, user.password))
    con.commit()
    return {"status": "Success", "message": "User registered successfully"}

@app.post('/signin')
def signin(username: str, password: str):
    user = UserModel(username, password)
    res = cur.execute("SELECT username, password FROM Users WHERE (username = ? and password = ?)", (user.username, user.password))
    user_record = res.fetchone()
    if user_record == None:
        return {"status": "Failure", "message": "User Password Incorrect"} 
    
    else:
        return {"status": "Success",  "message": "User successfully authenticated."}

@app.post('/follow')
def follow(user_id: str, follower_id: str):
    print(user_id, follower_id)
    res = cur.execute("SELECT username FROM Users WHERE (username = ?)", (user_id,))
    user = res.fetchone()
    user = user[0]
    followee_res = cur.execute("SELECT username FROM Users WHERE (username = ?)", (follower_id,))
    followee_res = followee_res.fetchone()
    followee_user = followee_res[0] if followee_res is not None else None
    if followee_res != None:
        cur.execute("INSERT INTO Followers (username, followee_id) VALUES (?, ?)", (user, followee_user))
        con.commit()
        return {"status": "Success", "message": f"You Succesfully Followed {followee_user}"}

    else:
        return {"status": "Failure", "message": "This Person You are trying to follow does not exist"}  








    

