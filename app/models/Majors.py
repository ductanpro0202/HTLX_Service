from extension import db

class Majors(db.Model):
    __tablename__ = 'majors'

    majorsID = db.Column(db.String(10), primary_key=True, nullable=False)
    majorsName = db.Column(db.String(100), unique=True, nullable=False)
    department_id = db.Column(db.String(10), nullable=False)

    # Additional fields if needed

    def save(self):
        db.session.add(self)
        db.session.commit()
