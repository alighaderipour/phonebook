from . import db

class Jobs(db.Model):
    __tablename__ = 'Jobs'
    JobID = db.Column(db.Integer, primary_key=True)
    JobTitle = db.Column(db.String(100), nullable=False)
    SectionID = db.Column(db.Integer, db.ForeignKey('Sections.SectionID'), nullable=False)
    phone_numbers = db.relationship('PhoneNumbers', backref='job', cascade='all, delete')
    users = db.relationship('Users', backref='job')

class Sections(db.Model):
    __tablename__ = 'Sections'
    SectionID = db.Column(db.Integer, primary_key=True)
    SectionName = db.Column(db.String(100), unique=True, nullable=False)
    Description = db.Column(db.String(255))
    jobs = db.relationship('Jobs', backref='section', cascade='all, delete')
    users = db.relationship('Users', backref='section')

class PhoneTypes(db.Model):
    __tablename__ = 'PhoneTypes'
    PhoneTypeID = db.Column(db.Integer, primary_key=True)
    PhoneTypeName = db.Column(db.String(30), unique=True, nullable=False)


class PhoneNumbers(db.Model):
    __tablename__ = 'PhoneNumbers'
    PhoneID = db.Column(db.Integer, primary_key=True)
    JobID = db.Column(db.Integer, db.ForeignKey('Jobs.JobID'), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    PhoneTypeID = db.Column(db.Integer, db.ForeignKey('PhoneTypes.PhoneTypeID'))
    phone_type = db.relationship("PhoneTypes", backref="phone_numbers", lazy=True)


class Users(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    SectionID = db.Column(db.Integer, db.ForeignKey('Sections.SectionID'), nullable=False)
    JobID = db.Column(db.Integer, db.ForeignKey('Jobs.JobID'), nullable=False)
    Mobile = db.Column(db.String(11))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    password = db.Column(db.String(255))