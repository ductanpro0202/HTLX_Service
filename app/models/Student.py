from extension import db
from sqlalchemy import Unicode
class SinhVien(db.Model):    
    __tablename__ = 'sinh_vien'  # Tên bảng trong cơ sở dữ liệu
    
    studentID = db.Column(db.Integer, primary_key=True, nullable= False,unique=True)
    fullName = db.Column(Unicode(100),nullable=False)
    dob = db.Column(db.String(10), nullable=False)  # Sử dụng kiểu String cho ngày tháng
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phoneNumber = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    classID = db.Column(db.String(20), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
