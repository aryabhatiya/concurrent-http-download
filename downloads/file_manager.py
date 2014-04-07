from downloads import db
from downloads import log
import time
import os
import datetime


class Filemanager(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    location = db.Column(db.String(256))
    filename = db.Column(db.String(128))
    isdownloaded = db.Column(db.Integer,default=0)
    splits = db.Column(db.Integer,default=10)
    size = db.Column(db.Integer,default=0)
    block = db.Column(db.Integer,default=1490)
    total_sectors = db.Column(db.Integer,default=0)
    infs = db.Column(db.Integer,default=0)
    starttime = db.Column(db.Integer,default=0)
    endtime = db.Column(db.Integer,default=0)
    sectors = db.relationship('Sector', backref = 'fname', lazy = 'dynamic')

    partialsize = 0
    def __init__(self):
        pass

    def infs(self,path,filename):
        data = self.query.filter_by(location = path, filename = filename ).first()
        return data

    def add(self,path,filename):
        self.location = path
        self.filename = filename
        self.starttime = time.time()
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

    def writefs(self,data,offset=0):
        fl = self.location + '/' + self.filename
        prm = 'w'
        if os.path.exists(fl):
            prm = 'r+b'            
        with open(fl,prm) as f:
            f.seek(offset)
            f.write(data)
            
    def merge_sectors(self):
        with open(self.name(), "wb") as outfile:
            for sector in self.sectors.all():
                with open(sector.name(), "rb") as infile:
                    outfile.write(infile.read())
        self.infs = 1 
        self.endtime = time.time()
        self.update()
        log(self)


    def add_sectors(self):
        i = 0
        j = 0
        self.block = self.size / 16
        while i <= self.size:
            end = i + self.block
            if  end >= self.size:
                end = self.size
            Sector.add(i,end,self)
            i +=  self.block
            j += 1
        self.total_sectors = j
        self.update()
        return j

    def name(self):
        return  str(self.location)  + self.filename

    
    def __repr__(self):
#        f = lambda x: x == 1 and ' download complete' or ' download incomplete ' 
        finfs = lambda x: x == 1 and ' in FileSystem ' +  ' time taken: ' + str(datetime.timedelta(self.endtime - self.starttime))   or '' 
        dratio = 0
        if self.size:
            dratio =  (self.partialsize*100)/self.size
        return self.filename + ' total size: ' + str(self.size) + \
            ' downloaded  (' + str(dratio) + "%)" +  finfs(self.infs) 

            
    
class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    start = db.Column(db.Integer,default=0)
    end = db.Column(db.Integer,default=0)
    isdownloaded = db.Column(db.Integer,default=0)
    size = db.Column(db.Integer,default=0)
    file_id = db.Column(db.Integer, db.ForeignKey('filemanager.id'))
    

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def add(self,start,end,filestat):
        sec = Sector(start = start, end = end , size = end - start, fname = filestat)
        db.session.add(sec)
        db.session.commit()
        return sec

    def name(self):
        return self.fname.location + "/." + str(self.id) + "_" + self.fname.filename

    def write(self,data):
        with open(self.name(),"w") as f:
            f.write(data)
 
    def __repr__(self):
        f = lambda x: x == 1 and ' donwloaded' or ' not downloaded' 
        return str(self.id) + ": " + self.fname.location + "/" + self.fname.filename + ": " + "offset :" \
            + str(self.start) + '-' + str(self.end) +  f(self.isdownloaded)
    
    
