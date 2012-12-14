
##Core table where status change is recorded##
create_state_change = '''CREATE TABLE "state_change" (
    "timestamp" INTEGER NOT NULL,
    "new_state" INTEGER NOT NULL
);'''

#Primary daily reports table
create_daily_reports = '''CREATE TABLE daily_reports (
    "date" INTEGER NOT NULL,
    "on" INTEGER NOT NULL
);'''

#Consolidated reports table
create_reports = '''CREATE TABLE "reports" (
    "date" INTEGER NOT NULL,
    "type" INTEGER NOT NULL,
    "on" INTEGER NOT NULL
);'''


#messages table
create_messages = '''CREATE TABLE "messages" (
    "new_state" INTEGER NOT NULL,
    "message" TEXT NOT NULL,
    "frequency" INTEGER NOT NULL DEFAULT (0)
)'''

#used in case of Internet connectivity problem 
create_tweet_queue = '''CREATE TABLE "tweet_queue" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "type" INTEGER NOT NULL DEFAULT (1),
    "message" TEXT NOT NULL,
    "picture" TEXT NOT NULL,
    "timestamp" INTEGER NOT NULL,
    "expires" INTEGER NOT NULL
);'''
