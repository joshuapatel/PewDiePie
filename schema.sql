CREATE TABLE IF NOT EXISTS econ (
    coins BIGINT NOT NULL,
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    transfer BOOL DEFAULT false NOT NULL,
    uses INT DEFAULT 0 NOT NULL
);

CREATE TABLE IF NOT EXISTS econshop (
    roleid BIGINT NOT NULL UNIQUE,
    guildid BIGINT NOT NULL,
    reqamount BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS prefixes (
    guildid BIGINT NOT NULL,
    prefix varchar(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS shovel (
    name TEXT NOT NULL,
    fate BOOL NOT NULL,
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS crime (
    name TEXT NOT NULL,
    fate BOOL NOT NULL,
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS snipe (
    contents TEXT NOT NULL,
    usr BIGINT NOT NULL,
    guild BIGINT NOT NULL,
    channel BIGINT NOT NULL,
    message BIGINT NOT NULL UNIQUE,
    bot BOOL NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS subgap (
    msgid BIGINT NOT NULL UNIQUE,
    channelid BIGINT NOT NULL UNIQUE,
    guildid BIGINT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS subgapbackup (
    msgid BIGINT NOT NULL,
    channelid BIGINT NOT NULL,
    guildid BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS sub_setup (
    guildid BIGINT NOT NULL UNIQUE,
    first_ch TEXT NOT NULL,
    second_ch TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS warns (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    issuerid BIGINT NOT NULL,
    issuername TEXT NOT NULL,
    reason TEXT NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS daily (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS weekly (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS fbblocked (
    userid BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS blacklisted (
    userid BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS apikeys (
    dankmemer TEXT NOT NULL,
    openweathermap TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS donator (
    userid BIGINT NOT NULL,
    level BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS polls (
    guildid BIGINT NOT NULL,
    channelid BIGINT NOT NULL,
    messageid BIGINT NOT NULL,
    executorid BIGINT NOT NULL,
    polltext TEXT NOT NULL,
    pollid TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    challengename TEXT NOT NULL,
    challengetype TEXT NOT NULL,
    challengeid SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS coinpermin (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS economy (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    lvl BIGINT NOT NULL,
    xp BIGINT NOT NULL
);