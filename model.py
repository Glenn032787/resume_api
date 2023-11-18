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

with app.app_context():
   db.create_all()
