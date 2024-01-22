from extension import db

class Department(db.Model):
    __tablename__ = 'department'

    departmentID = db.Column(db.String(10), primary_key=True, nullable=False)
    departmentName = db.Column(db.String(100), nullable=False)

    # Additional fields if needed

    def save(self):
        db.session.add(self)
        db.session.commit()
