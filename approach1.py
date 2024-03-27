from fastapi import FastAPI
import json
import sqlite3
from datetime import datetime, timezone
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

"""
Dont really need signup or signin, just wanted to allow users to sign in to be able
to test the GET timelines of different users without overcomplicating anything. 
Obviously in production, this is not how I would Authenticate Users or store passwords etc...

"""
@app.post('/signup')
def register(username:str, password:str):
    "Check if Username Already Exists"
    user = cur.execute("SELECT username FROM Users WHERE (username = (?))", (username,))
    if user != None:
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
    
"""
The Follow API is a very simple implementation to allow Users to follow other active Users.  
This is similar to what is described in DDIA IF twitter used a relational Database.  However, 
that is definitely not true in practice as they definitley use some type of Graph-DB. 

"""

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
Update is what Twitter calls what we think of as Tweeting in their API Documentation.  (somewhat confusing
naming)
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
    
"""
get_timeline in this naive approach has some fundamental problems as illustrated in DDIA.  When a user 
requests their home timeline, all the tweets of the people they follow are looked up and merged and then 
sorted by time.  The first version of Twitter used this approach, but the systems struggled to keep up
with the crazy amount of get_timeline requests.  According to DDIA, the home timeline was 300k requests/s
in 2012 while the post tweet or (update) was only 4.6k requests per second.  So Twitter had a lot more
home timeline requests then post tweet requests which makes sense. Approach2.py has the optimization they 
went with to prioritize the get_timeline operation.  

Again, there are certain things about this that I would change in a real production example.  I would handle
the sorting logic in my SQL query rather than my application code and I would place some type of LIMIT on
the number of tweets returned.  (Most users on average only look through a small amount of recent tweets).
That being said I would also include some type of pagination so I am not sending huge amounts of tweets over
across the same network. 

"""

@app.get("/timeline")
def get_timeline(user_id):
    res = cur.execute("""SELECT user, tweet, timestamp FROM Tweets WHERE user IN(
                        SELECT followee FROM Following WHERE (follower = ?))""", (user_id,))
    tweets = res.fetchall()
    array = []
    categories = ["Username", "Tweet", "Time"]
    for tweet in tweets:
         array.append([
            [categories[0], tweet[0]],
            [categories[1], tweet[1]],
            [categories[2], tweet[2]],
        ])
         
    time_sorted_array = sorted(array, key=lambda tweet_objects: tweet_objects[2][1], reverse=True)

    print(time_sorted_array)

    for tweet in time_sorted_array:
        tweet[2][1] = datetime.fromtimestamp(tweet[2][1]).strftime('%Y-%m-%d %H:%M:%S')  
    """
    These are now sorted by most recent tweets, however this is quite costly.  
    n(log(n)) on potentially a large number of tweets
    """
    json_object = json.dumps(time_sorted_array)
    return json_object

    


    






