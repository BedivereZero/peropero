CREATE TABLE users(
    userid      INTEGER     NOT NULL,
    name        VARCHAR     NOT NULL,
    PRIMARY KEY (userid)
);

CREATE TABLE images(
    imageid     VARCHAR(64) NOT NULL,
    userid      INTEGER     NOT NULL,
    url         VARCHAR(64) NOT NULL,
    download    BOOLEAN     NOT NULL DEFAULT 0,
    PRIMARY KEY (imageid),
    FOREIGN KEY (userid) REFERENCES users(userid)
);
