from extension import db

class Class(db.Model):

    __tablename__ = 'class'
    
    classID = db.Column(db.String(1), primary_key=True, nullable=False)
    className = db.Column(db.String(100),  nullable=False)
    majorsID = db.Column(db.String(10), nullable=False)
    classSize = db.Column(db.Integer, nullable=True)  # Assuming Classize can be nullable
    

    def save(self):
        db.session.add(self)
        db.session.commit()
