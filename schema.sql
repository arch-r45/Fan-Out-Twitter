CREATE TABLE "Users" (
    "username" TEXT, 
    "password" TEXT NOT NULL,
    PRIMARY KEY("username")
);

CREATE TABLE "Following" (
    "follower" TEXT NOT NULL,
    "followee" TEXT NOT NULL,
    FOREIGN KEY("follower") REFERENCES "Users"("username"),
    FOREIGN KEY("followee") REFERENCES "Users"("username")
);


