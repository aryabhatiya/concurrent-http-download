import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'downloader.db')
#SQLALCHEMY_DATABASE_URI='mysql://root:bangla@localhost/downloader'
