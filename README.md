# Twitter Naive Fan Out Implementation Followed by Optimization

## Background and Introduction

In Designing Data Intensive Applications, Martin Kleppmann dives into the early struggles of Twitters scaling and an optimization Twitter made to improve performance.  This centered around two of Twitters main operations: Post Tweet, and Home Timeline.  Post Tweet averaged 4.6k requests/sec and Home Timeline averaged 300k requests/sec.  This is a fairly small number of writes but a much greater number of reads.  (This makes perfect sense as much more people are viewing tweets at a given time than actively tweeting) He described this problem as _fan out_, as in order to serve one incoming request, you need to make many other requests to other services.  In Twitter's case, each user follows many people and each user is followed by many other people.  


In this repository, I implement both approaches that twitter had to handling the _fan out_ problem and package these into a simple FASTAPI micro backend to experiment with the requests.  I wanted to focus pretty much entirely on the two API's update and get_timeline to recreate what Twitter did in both scenarios.  If this were being pushed to production, I would improve some of the other aspects like the user authentication and store MUCH more in the database but I left those as lightweight as possible to focus entirely on the core objective.  I also choose to write SQL inline and constantly flipped between SQL and Python in my application code rather than using an Object Relational Mapper.  This was simply to better articulate what was going on in the Database with the queries.  


### Approach 1: Relational Database


Early Twitter choose to post a tweet into a database table that consisted of tweets.  When a user wanted to get their home timeline, which needs to return a large list of recent tweets, the backend needed to look up all the people the user followed, find all the tweets for each user, and sort on merge.  Early stage Twitter's servers could not handle this load and deliver tweets fast and efficient.  (Twitter aims for tweets to followers in 4 seconds)

Martin describes how this is implemented and provided a dummy SQL query that could accomplish this.  

```sql
SELECT tweets.*, users.* FROM tweets
JOIN users ON tweets.sender_id = users.id JOIN follows ON follows.followee_id = users.id WHERE follows.follower_id = current_user
```

In my application, I choose to use subqueries and made some minor changes to work with the rest of my application but it's accomplishing more or less the same thing. 

```sql 
SELECT user, tweet, timestamp FROM Tweets 
WHERE user IN(
    SELECT followee FROM Following 
    WHERE (follower = user)
    ),
```

![alt text][twitter]

[twitter]: https://github.com/arch-r45/Fan-Out-Twitter/blob/main/pictures/Twitter-relational.png


I implement this in approach1.py and to run locally see below.  
```bash
uvicorn approach1:app --reload
```

This is obviously very expensive with the large amount of reads, so we have to ask, can we do better? Twitter has the answer in approach 2, with using an in memory cache to store a list of tweets for each recipient user.  Everytime a user tweets something, look up all the people they follow and write a new tweet to their cache.  This obviously has a major advantage: not having to make a disk seek everytime a user wants to get their home timeline.  For twitter the most important load parameter is ensuring users get their home timeline as fast as possible.  If it takes a little longer to send a tweet to ensure users get their tweets fast, thats a tradeoff that is worth making, as there are way more requests to get tweets then to send tweets. 



![alt text][twitter2]

[twitter2]: https://github.com/arch-r45/Fan-Out-Twitter/blob/main/pictures/twitter-redis-2.png



I choose to use Redis to implement the cache, and this application code can be seen in approach2.py and can be ran locally using the following command. 

```bash
uvicorn approach2:app --reload
```









