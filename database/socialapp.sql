DROP TABLE IF EXISTS post_tag CASCADE;
DROP TABLE IF EXISTS likes CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS follower CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS tag CASCADE;
DROP TABLE IF EXISTS users CASCADE;


CREATE TABLE users(

    userid VARCHAR(255) PRIMARY KEY,

    username VARCHAR(255)
    UNIQUE
    NOT NULL,

    email VARCHAR(255)
    UNIQUE
    NOT NULL,

    password TEXT
    NOT NULL,

    fullname VARCHAR(255),

    bio TEXT,

    profpicurl TEXT,

    createdat TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE posts(

    postid VARCHAR(255)
    PRIMARY KEY,

    userid VARCHAR(255)
    NOT NULL,

    imageurl TEXT
    NOT NULL,

    caption TEXT,

    fullname VARCHAR(255),

    createdat TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_posts_user
    FOREIGN KEY(userid)
    REFERENCES users(userid)
    ON DELETE CASCADE
);


CREATE TABLE comments(

    comid VARCHAR(255)
    PRIMARY KEY,

    postid VARCHAR(255)
    NOT NULL,

    userid VARCHAR(255)
    NOT NULL,

    commtxt TEXT
    NOT NULL,

    createdat TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_comments_post
    FOREIGN KEY(postid)
    REFERENCES posts(postid)
    ON DELETE CASCADE,

    CONSTRAINT fk_comments_user
    FOREIGN KEY(userid)
    REFERENCES users(userid)
    ON DELETE CASCADE
);


CREATE TABLE likes(

    likeid VARCHAR(255)
    PRIMARY KEY,

    postid VARCHAR(255)
    NOT NULL,

    userid VARCHAR(255)
    NOT NULL,

    createdat TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_likes_post
    FOREIGN KEY(postid)
    REFERENCES posts(postid)
    ON DELETE CASCADE,

    CONSTRAINT fk_likes_user
    FOREIGN KEY(userid)
    REFERENCES users(userid)
    ON DELETE CASCADE
);


CREATE TABLE follower(

    followid VARCHAR(255)
    PRIMARY KEY,

    followerid VARCHAR(255)
    NOT NULL,

    followeeid VARCHAR(255)
    NOT NULL,

    createdat TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT unique_follow
    UNIQUE(followerid,followeeid),

    CONSTRAINT fk_follower_user
    FOREIGN KEY(followerid)
    REFERENCES users(userid)
    ON DELETE CASCADE,

    CONSTRAINT fk_followee_user
    FOREIGN KEY(followeeid)
    REFERENCES users(userid)
    ON DELETE CASCADE
);


CREATE TABLE tag(

    tagid VARCHAR(255)
    PRIMARY KEY,

    tagname VARCHAR(255)
    UNIQUE
    NOT NULL
);


CREATE TABLE post_tag(

    postid VARCHAR(255)
    NOT NULL,

    tagid VARCHAR(255)
    NOT NULL,

    PRIMARY KEY(postid,tagid),

    CONSTRAINT fk_posttag_post
    FOREIGN KEY(postid)
    REFERENCES posts(postid)
    ON DELETE CASCADE,

    CONSTRAINT fk_posttag_tag
    FOREIGN KEY(tagid)
    REFERENCES tag(tagid)
    ON DELETE CASCADE
);


CREATE INDEX idx_users_username
ON users(username);

CREATE INDEX idx_users_email
ON users(email);

CREATE INDEX idx_posts_userid
ON posts(userid);

CREATE INDEX idx_comments_postid
ON comments(postid);

CREATE INDEX idx_likes_postid
ON likes(postid);

CREATE INDEX idx_follower_followerid
ON follower(followerid);

CREATE INDEX idx_follower_followeeid
ON follower(followeeid);