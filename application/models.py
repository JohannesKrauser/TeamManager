from application.database import db


class Employee(db.Model):
    __tablename__ = "Employees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gid = db.Column(db.String(50), unique=True, nullable=False)
    local_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    time_tracks = db.relationship("TimeTrack", backref="employee", lazy=True)

    def __repr__(self):
        return f"{self.name} {self.last_name}"


class Project(db.Model):
    __tablename__ = "Projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    accounts = db.relationship("Account", backref="project", lazy=True)

    def __repr__(self):
        return f"{self.name}"


class Account(db.Model):
    __tablename__ = "Accounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    order_amount = db.Column(db.Float, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("Projects.id"), nullable=False)
    time_tracks = db.relationship("TimeTrack", backref="account", lazy=True)

    def __repr__(self):
        return f"{self.name}"


class TimeTrack(db.Model):
    __tablename__ = "TimeTracks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employees.id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("Accounts.id"), nullable=False)

    def __repr__(self):
        return f"{self.hours}"
