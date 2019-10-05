-- Economy table for storing coin information
CREATE TABLE IF NOT EXISTS econ (
    coins BIGINT NOT NULL,
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    transfer BOOL DEFAULT false NOT NULL,
    uses INT DEFAULT 0 NOT NULL
);

-- Economy shop
CREATE TABLE IF NOT EXISTS econshop (
    roleid BIGINT NOT NULL UNIQUE,
    guildid BIGINT NOT NULL,
    reqamount BIGINT NOT NULL
);

-- Custom bot prefixes
CREATE TABLE IF NOT EXISTS prefixes (
    guildid BIGINT NOT NULL UNIQUE,
    prefix varchar(30) NOT NULL
);

-- Shovel messages
CREATE TABLE IF NOT EXISTS shovel (
    name TEXT NOT NULL,
    fate BOOL NOT NULL,
    id SERIAL PRIMARY KEY
);

-- Crime messages
CREATE TABLE IF NOT EXISTS crime (
    name TEXT NOT NULL,
    fate BOOL NOT NULL,
    id SERIAL PRIMARY KEY
);

-- Snipe messages and information
CREATE TABLE IF NOT EXISTS snipe (
    contents TEXT NOT NULL,
    usr BIGINT NOT NULL,
    guild BIGINT NOT NULL,
    channel BIGINT NOT NULL,
    message BIGINT NOT NULL UNIQUE,
    bot BOOL NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Guild snipe settings
CREATE TABLE IF NOT EXISTS guildsnipesettings (
    guildid BIGINT NOT NULL,
    snipeenabled BOOL NOT NULL
);

-- User warnings
CREATE TABLE IF NOT EXISTS warns (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    issuerid BIGINT NOT NULL,
    issuername TEXT NOT NULL,
    reason TEXT NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Stores the next time a user can use the daily command
CREATE TABLE IF NOT EXISTS daily (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Stores the next time a user can use the weekly command
CREATE TABLE IF NOT EXISTS weekly (
    userid BIGINT NOT NULL,
    guildid BIGINT NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Stores users blacklisted from p.feedback
CREATE TABLE IF NOT EXISTS fbblocked (
    userid BIGINT NOT NULL
);

-- Stores blacklisted users
CREATE TABLE IF NOT EXISTS blacklisted (
    userid BIGINT NOT NULL UNIQUE
);

-- API keys
CREATE TABLE IF NOT EXISTS apikeys (
    dankmemer TEXT NOT NULL,
    openweathermap TEXT NOT NULL
);

-- Stores the donators
CREATE TABLE IF NOT EXISTS donator (
    userid BIGINT NOT NULL,
    level BIGINT NOT NULL
);

-- Stores the active polls
CREATE TABLE IF NOT EXISTS polls (
    guildid BIGINT NOT NULL,
    channelid BIGINT NOT NULL,
    messageid BIGINT NOT NULL,
    executorid BIGINT NOT NULL,
    polltext TEXT NOT NULL,
    pollid TEXT NOT NULL
);

-- Stores challenges for the p.challenge command
CREATE TABLE IF NOT EXISTS challenges (
    challengename TEXT NOT NULL,
    challengetype TEXT NOT NULL,
    challengeid SERIAL PRIMARY KEY
);

-- Stores people for the p.ask command
CREATE TABLE IF NOT EXISTS askpeople (
    name TEXT NOT NULL
);