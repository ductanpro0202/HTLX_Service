from extension import db
from sqlalchemy import  Float

class Grade(db.Model):    
    __tablename__ = 'grade'  # Tên bảng trong cơ sở dữ liệu
    
    gradeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    studentID = db.Column(db.Integer,  nullable=False)
    courseID = db.Column(db.String(20), nullable=False)
    midtermScore = db.Column(Float, nullable=False)
    attendance = db.Column(db.Float, nullable=False)
    finalScore = db.Column(db.Float, nullable=False)
    schoolYear = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    averageScore = db.Column(db.Float)

    def save(self):
        db.session.add(self)
        db.session.commit()
