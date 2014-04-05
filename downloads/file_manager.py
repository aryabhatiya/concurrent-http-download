from downloads import db
class FileManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256))
    filename = db.Column(db.String(128))
    isdownloaded = db.Column(db.Integer,default=0)
    splits = db.Column(db.Integer,default=10)
    size = db.Column(db.Integer,default=0)
    partial = db.Column(db.Integer,default=0)
    def __init__(self):
        pass
    def infs(self,path,filename):
        return self.query.filter_by(location = path, filename = filename ).first()
    
    
    
