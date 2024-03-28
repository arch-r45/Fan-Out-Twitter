from fastapi import FastAPI
import json
import sqlite3
from datetime import datetime, timezone
app = FastAPI()
con = sqlite3.connect("approach2.db", check_same_thread=False)
cur = con.cursor()
import redis
r = redis.Redis(host='localhost', port=6380, decode_responses=True)
"""
Some of this is very similar logic to approach1.py.  The real changes between the two 
are  with the update API and the get_timeline API 
"""
class UserModel():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tweets = []
        self.following = []
        self.followers = []
@app.post('/signup')
def register(username:str, password:str):
    user = cur.execute("SELECT username FROM Users WHERE (username = (?))", (username,))
    user_name= user.fetchall()
    if user_name != []:
        return {"status": "Failure", "message": "Username already exists!"}
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
        followers = cur.execute("SELECT follower FROM Following WHERE (followee = ?)", (user, ))
        followers_to_cache = followers.fetchall()
        data_to_cache = json.dumps((user, timestamp, tweet))
        for f in followers_to_cache:
            r.rpush(f[0], data_to_cache)
        return {"status": "Success", "message": "Nice Tweet!"}
    else:
        return {"status": "Failure", "message": "Tweet Unsuccesful"} 
    
@app.get("/timeline")
def get_timeline(user_id):
    tweets = r.lrange(user_id, 0, -1)
    tweets_deserialized = [json.loads(tweet) for tweet in tweets]
    array = []
    categories = ["Username", "Time", "Tweet"]
    for i in range(len(tweets_deserialized)):
        array.append([
            [categories[i], tweets_deserialized[i][0]],
            [categories[1], int(tweets_deserialized[i][1])],
            [categories[2], tweets_deserialized[i][2]],
        ])
    time_sorted_array = sorted(array, key=lambda tweet_objects: tweet_objects[2][1], reverse=True)
    for tweet in time_sorted_array:
        tweet[1][1] = datetime.fromtimestamp(tweet[1][1]).strftime('%Y-%m-%d %H:%M:%S')  
    json_object = json.dumps(time_sorted_array)
    return json_object