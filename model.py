from database import db, ma, app

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

class EducationSchema(ma.Schema):
    class Meta:
        fields = ("id", "university", "location", "degree", "startDate", "endDate", "gpa")
        model = Education

education_schema = EducationSchema()
education_multischema = EducationSchema(many = True)

#######
# Email
#######

class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    emailType = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return f'<Email: {self.type}>'

class EmailSchema(ma.Schema):
    class Meta:
        fields = ("id", "emailType", "email")
        model = Email

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

class LinkSchema(ma.Schema):
    class Meta:
        fields = ("id", "linkType", "link")
        model = Link

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

class TranscriptSchema(ma.Schema):
    class Meta:
        fields = ("id", "school", "courseCode", "courseTitle", "grade", "semester")
        model = Transcript

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

class PublicationSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "journal", "doi", "date", "status")
        model = Publication

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

class WorkSchema(ma.Schema):
    class Meta:
        fields = ("id", "jobTitle", "company", "location", "startDate", "endDate")
        model = Work

work_schema = WorkSchema()
work_multischema = WorkSchema(many = True)

with app.app_context():
   db.create_all()
