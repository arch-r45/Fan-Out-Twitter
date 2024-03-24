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
from datetime import datetime
app = FastAPI()
con = sqlite3.connect("base.db", check_same_thread=False)
cur = con.cursor()
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
        cur.execute("INSERT INTO Following (follower, followee) VALUES (?, ?)", (user, followee_user))
        con.commit()
        return {"status": "Success", "message": f"You Succesfully Followed {followee_user}"}
    else:
        return {"status": "Failure", "message": "This Person You are trying to follow does not exist"} 



"""
Update is what Twitter calls what we think of as Tweeting in their API Documentation
""" 
@app.post('/update')
def update(user_id: str, tweet: str):
    res = cur.execute("SELECT username FROM Users WHERE (username = ?)", (user_id,))
    user = res.fetchone()
    user = user[0]
    curr_dt = datetime.now() 
    timestamp = int(round(curr_dt.timestamp()))

    if user:
        cur.execute("INSERT INTO Tweets(user, timestamp, tweet) VALUES (?, ?, ?)", (user, timestamp, tweet))
        con.commit()
        return {"status": "Success", "message": "Nice Tweet!"}
    
    else:
        return {"status": "Failure", "message": "Tweet Unsuccesful"} 


@app.get("/timeline")
def get_timeline(user_id):
    res = cur.execute("""SELECT user, tweet, timestamp FROM Tweets WHERE user IN(
                        SELECT followee FROM Following WHERE (follower = ?))""", (user_id,))
    
    tweets = res.fetchall()
    print(tweets)
    return {"status": "Success", "message": "Success"}

    


    






