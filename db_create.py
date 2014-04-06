#!flask/bin/python
from downloads import db
import subprocess
# import downloader
# def prepare():
#     subprocess.call(["rm", "downloader.db"])
#     subprocess.call(["rm", "/usr/local/src/testdownload/downloads.rss"])
#     db.create_all()

# def runmachine(tr=True):
#     downloader.testcase(tr)
    

# if __name__ == "main":
# #    prepare()
db.create_all()
