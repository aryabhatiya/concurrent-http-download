from downloads import db
from downloads import log
class FileManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256))
    filename = db.Column(db.String(128))
    isdownloaded = db.Column(db.Integer,default=0)
    splits = db.Column(db.Integer,default=10)
    size = db.Column(db.Integer,default=0)
    partial = db.Column(db.Integer,default=0)
    block = db.Column(db.Integer,default=0)
    def __init__(self):
        pass

    def infs(self,path,filename):
        data = self.query.filter_by(location = path, filename = filename ).first()
        return data

    def add(self,path,filename):
        self.location = path
        self.filename = filename
        db.session.add(self)
        db.session.commit()
        return self
    def query_update(self,path,filename,block):
        data = self.infs(path,filename)
        data.block = data.block + 1 
        db.session.add(data)
        db.session.commit()
        return data

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def writefs(self,data):
        with open(self.location + '/' + self.filename,'a') as f:
            f.write(data)
    
    def status(self,param):
        if self.isdownloaded == 1:
            log(param + ": " + self.filename + ' is alaready there.')
            return
        log(param + ": " +  self.filename + ' total size: ' + str(self.size) + ' downloaded: ' + str((self.size/self.splits)*self.partial))

            
    
    
