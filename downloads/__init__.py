from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db =SQLAlchemy(app)

from downloads import file_manager
from file_downloader import FileDownloader

Downloads = FileDownloader()


