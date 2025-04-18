import os

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://hamzann:hamza00@cluster0.id2lo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "TeraboxVideosRoBot")

#Shortner (token system) 
# check my discription to help by using my refer link of shareus.io


SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "inShortUrl.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "2e7e4739d495b5fce0531b9dc8342c40762a3fa9")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 86400)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/ChipsTutorial/7") # shareus ka 
