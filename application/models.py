from application.database import db


class Employee(db.Model):
    __tablename__ = "Employees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gid = db.Column(db.String(50), unique=True, nullable=False)
    local_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"{self.name} {self.last_name}"
