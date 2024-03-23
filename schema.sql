CREATE TABLE "Users" (
    "username" TEXT, 
    "password" TEXT NOT NULL,
    PRIMARY KEY("username")
);

CREATE TABLE "Following" (
    "follower" TEXT,
    "followee" TEXT,
    FOREIGN KEY("follower") REFERENCES "Users"("username"),
    FOREIGN KEY("followee") REFERENCES "Users"("username")
);


CREATE TABLE "Tweets" (
    "user" TEXT,
    "time" INTEGER,
    "date" INTEGER,
    "tweet" TEXT,
    FOREIGN KEY("user") REFERENCES "Users"("username")
);





