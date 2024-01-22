from extension import db

class Course(db.Model):
    __tablename__ = 'course'

    courseID = db.Column(db.String(10), primary_key=True, nullable=False)
    courseName = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    # Additional fields if needed

    def save(self):
        db.session.add(self)
        db.session.commit()
