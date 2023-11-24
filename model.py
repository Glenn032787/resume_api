from database import db, ma, app
from marshmallow import fields
from datetime import datetime
#######
# Education
#######

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String)
    location = db.Column(db.String)
    degree = db.Column(db.String)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    gpa = db.Column(db.Float)

    def __repr__(self):
        return f'<{self.university}>'

class EducationResponseSchema(ma.SQLAlchemySchema):
   
    startDate = fields.Str(example = "2017-01-09")
    endDate = fields.Str(example = "2023-09-01")

    class Meta:
        fields = ("id", "university", "location", "degree", "startDate", "endDate", "gpa")
        model = Education
        include_fk = True
        #datetimeformat = '%Y-%m-%d'
    
education_schema = EducationResponseSchema()
education_multischema = EducationResponseSchema(many = True)

#######
# Email
#######

class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    emailType = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<Email: {self.emailType}>'

class EmailSchema(ma.Schema):
    class Meta:
        fields = ("id", "emailType", "email")
        model = Email
        include_fk = True
        load_instance = True,
        sqla_session = db.session
        
    emailType: fields.String(required = True)
    email: fields.Email(required = True)
    id: fields.Integer()
    

email_schema = EmailSchema()
email_multischema = EmailSchema(many = True)

######
# Link
######

class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key = True)
    linkType = db.Column(db.String, unique = True)
    link = db.Column(db.String, unique = True)

    def __repr__(self):
        return f"<Link: {self.linkType}>"

class LinkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "linkType", "link")
        model = Link
        include_fk = True

link_schema = LinkSchema()
link_multischema = LinkSchema(many = True)

######
# Transcript
######

class Transcript(db.Model):
    __tablename__ = "transcript"
    id = db.Column(db.Integer, primary_key = True)
    school = db.Column(db.Integer, db.ForeignKey(Education.id))
    courseCode = db.Column(db.String, unique = True)
    courseTitle = db.Column(db.String)
    grade = db.Column(db.Integer)
    semester = db.Column(db.Integer)

    def __repr__(self):
        return f"<Transcript: {self.courseCode}>"

class TranscriptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "school", "courseCode", "courseTitle", "grade", "semester")
        model = Transcript
        include_fk = True

transcript_schema = TranscriptSchema()
transcript_multischema = TranscriptSchema(many = True)

######
# Publication
######
class Publication(db.Model):
    __tablename__ = "publication"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    journal = db.Column(db.String)
    doi = db.Column(db.String)
    date = db.Column(db.Date)
    status = db.Column(db.String)

    def __repr__(self):
        return f"<Publication: {self.journal}>"

class PublicationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "title", "journal", "doi", "date", "status")
        model = Publication
        include_fk = True

    doi = fields.Url()
    date = fields.Str(example = "2017-01-09")


publication_schema = PublicationSchema()
publication_multischema = PublicationSchema(many = True)

######
# Work
######
class Work(db.Model):
    __tablename__ = "work"
    id = db.Column(db.Integer, primary_key = True)
    jobTitle = db.Column(db.String)
    company = db.Column(db.String)
    location = db.Column(db.String)
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)

    def __repr__(self):
        return f"<Work: self.jobTitle>"

class WorkSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "jobTitle", "company", "location", "startDate", "endDate")
        model = Work
        include_fk = True
    
    startDate = fields.Str(example = "2017-01-09")
    endDate = fields.Str(example = "2017-01-09")

work_schema = WorkSchema()
work_multischema = WorkSchema(many = True)

with app.app_context():
   db.create_all()
