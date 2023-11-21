from flask import Flask, request 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime
from model import *
from database import app, db, ma
from sqlalchemy import sql


api = Api(app)

class EducationListAll(Resource):
    def get(self):
        schools = Education.query.all()
        return education_multischema.dump(schools)
    
    def post(self):
        startDate = datetime.strptime(request.json["startDate"], '%Y%m%d').strftime("%Y-%m-%d")
        endDate = datetime.strptime(request.json["endDate"], '%Y%m%d').strftime("%Y-%m-%d")

        newSchool = Education(
            university = request.json['university'],
            location = request.json['location'],
            degree = request.json['degree'],
            startDate = sql.func.date(startDate),
            endDate = sql.func.date(endDate),
            gpa = request.json['gpa']
        )

        db.session.add(newSchool)
        db.session.commit()
        return education_schema.dump(newSchool)
    
class EducationFilterID(Resource):
    def get(self, educationID):
        school = Education.query.get_or_404(educationID)
        return education_schema.dump(school)
    
    def delete(self, educationID):
        school = Education.query.get_or_404(educationID)
        db.session.delete(school)
        db.session.commit()
        return '', 204

class EducationFilterLocation(Resource):
    def get(self, location):
        school = db.session.execute(
            db.select(Education).filter_by(location = location)
        ).scalar()
        return education_schema.dump(school)

class EducationFilterDate(Resource):
    def get(self, date):
        date = datetime.strptime(date, '%Y%m%d').strftime("%Y-%m-%d")
        school = db.session.execute(
            db.select(Education).filter(sql.func.date(Education.startDate) <= sql.func.date(date)).filter(sql.func.date(Education.endDate) >= sql.func.date(date))
        ).scalar()
        return education_schema.dump(school)


api.add_resource(EducationListAll, '/api/education')
api.add_resource(EducationFilterID, '/api/education/<int:educationID>')
api.add_resource(EducationFilterLocation, '/api/education/location/<string:location>')
api.add_resource(EducationFilterDate, '/api/education/date/<string:date>')


## Email
class EmailListAll(Resource):
    def get(self):
        emails = Email.query.all()
        return email_multischema.dump(emails)

    def post(self):

        newEmail = Email(
            emailType = request.json['emailType'],
            email = request.json['email']
        )
        
        db.session.add(newEmail)
        db.session.commit()
        return email_schema.dump(newEmail)

class EmailFilterID(Resource):
    def get(self, emailId):
        email = Email.query.get_or_404(emailId)
        return email_schema.dump(email)
    
    def delete(self, emailId):
        email = Email.query.get_or_404(emailId)
        db.session.delete(email)
        db.commit()
        return '', 204

class EmailFilterType(Resource):
    def get(self, emailType):
        email = db.session.execute(
            db.select(Email).filter(Email.emailType == emailType)
        ).scalar()

        return email_schema.dump(email)

api.add_resource(EmailListAll, '/api/email')
api.add_resource(EmailFilterID, '/api/email/<int:emailId>')
api.add_resource(EmailFilterType, '/api/email/<string:emailType>')

## Link
class LinkListAll(Resource):
    def get(self):
        links = Link.query.all()
        return link_multischema.dump(links)
    
    def post(self):
        newLink = Link(
            linkType = request.json['linkType'],
            link = request.json['link']
        )

        db.session.add(newLink)
        db.session.commit()
        return link_schema(newLink)        

class LinkFilterId(Resource):
    def get(self, LinkId):
        link = Link.query.get_or_404(LinkId)
        return link_schema(link)
    
    def delete(self, LinkId):
        link = Link.query.get_or_404(LinkId)
        db.session.delete(link)
        db.session.commit()
        return '', 204

class LinkFilterType(Resource):
    def get(self, linkType):
        link = db.session.execute(
            db.select(Link).filter(Link.linkType == linkType)
        ).scalar()
        return link_schema.dump(link)

api.add_resource(LinkListAll, "/api/link")
api.add_resource(LinkFilterId, "/api/link/<int:LinkId>")
api.add_resource(LinkFilterType, "/api/link/<string:linkType>")

# Transcript
class TranscriptListAll(Resource):
    def get(self):
        transcripts = Transcript.query.all()
        return transcript_multischema.dump(transcripts)
    
    id = db.Column(db.Integer, primary_key = True)
    school = db.Column(db.Integer, db.ForeignKey(Education.id))
    courseCode = db.Column(db.String, unique = True)
    courseTitle = db.Column(db.String)
    grade = db.Column(db.Integer)
    semester = db.Column(db.Integer)

    def post(self):
        newTranscript = Transcript(
            school = request.json['school'],
            courseCode = request.json['courseCode'],
            courseTitle = request.json['courseTitle'],
            grade = request.json['grade'],
            semester = request.json['semester']
        )

        db.session.add(newTranscript)
        db.session.commit()
        return transcript_schema(newTranscript)        

class TranscriptFilterId(Resource):
    def get(self, transcriptID):
        transcript = Transcript.query.get_or_404(transcriptID)
        return transcript_schema(transcript)
    
    def delete(self, transcriptID):
        transcript = Transcript.query.get_or_404(transcriptID)
        db.session.delete(transcript)
        db.session.commit()
        return '', 204

class TranscriptFilterSchool(Resource):
    def get(self, schoolID):
        transcripts = db.session.execute(
            db.select(Transcript).filter(Transcript.school == schoolID)
        ).scalars()
        return transcript_multischema.dump(transcripts)

class TranscriptFilterSchoolSemester(Resource):
    def get(self, schoolID, semester):
        transcripts = db.session.execute(
            db.select(Transcript).filter(Transcript.school == schoolID).filter(Transcript.semester == semester)
        ).scalars()
        return transcript_multischema.dump(transcripts)

class TranscriptFilterCourseCode(Resource):
    def get(self, courseCode):
        transcript = db.session.execute(
            db.select(Transcript).filter(Transcript.courseCode == courseCode)
        ).scalar()
        return transcript_schema.dump(transcript)

api.add_resource(TranscriptListAll, "/api/transcript")
api.add_resource(TranscriptFilterId, "/api/transcript/<int:transcriptID>")
api.add_resource(TranscriptFilterSchool, "/api/transcript/school/<int:schoolID>")
api.add_resource(TranscriptFilterSchoolSemester, "/api/transcript/school/<int:schoolID>_<int:semester>")
api.add_resource(TranscriptFilterCourseCode, "/api/transcript/courseCode/<string:courseCode>")

# Publication
class PublicationListAll(Resource):
    def get(self):
        publications = Publication.query.all()
        return publication_multischema.dump(publications)

    def post(self):
        date = datetime.strptime(request.json['date'], '%Y%m%d').strftime("%Y-%m-%d")
        newPublication = Publication(
            title = request.json['title'],
            journal = request.json['journal'],
            doi = request.json['doi'],
            date = sql.func.date(date) ,
            status = request.json['status'],
        )

        db.session.add(newPublication)
        db.commit()
        return publication_schema.dump(newPublication)

class PublicationFilterID(Resource):
    def get(self, publicationID):
        publication = Publication.query.get_or_404(publicationID)
        return publication_schema.dump(publication)

    def delete(self, publicationID):
        publication = Publication.query.get_or_404(publicationID)
        db.session.delete(publication)
        db.commit()
        return '', 204

class PublicationFilterStatus(Resource):
    def get(self, status):
        publications = db.session.execute(
            db.select(Publication).filter(Publication.status == status)
        ).scalars()

        return publication_multischema.dump(publications)

api.add_resource(PublicationListAll, "/api/publication")
api.add_resource(PublicationFilterID, "/api/publication/<int:publicationID>")
api.add_resource(PublicationFilterStatus, "/api/publication/<string:status>")

# Work
class WorkListAll(Resource):
    def get(self):
        work = Work.query.all()
        return work_multischema.dump(work)

    def post(self):
        startDate = datetime.strptime(request.json["startDate"], '%Y%m%d').strftime("%Y-%m-%d")
        endDate = datetime.strptime(request.json["endDate"], '%Y%m%d').strftime("%Y-%m-%d")

        newWork = Work(
            jobTitle = request.json["jobTitle"],
            company = request.json["company"],
            location = request.json["location"],
            startDate = sql.func.date(startDate),
            endDate = sql.func.date(endDate)
        )

        db.session.add(newWork)
        db.commit()
        return work_schema.dump(newWork)

class WorkFilterID(Resource):
    def get(self, workID):
        work = Work.query.get_or_404(workID)
        return work_schema.dump(work)
    
    def delete(self, workID):
        work = Work.query.get_or_404(workID)
        db.session.delete(work)
        db.commit()
        return '', 204

class WorkFilterDate(Resource):
    def get(self, date):
        workDate = datetime.strptime(date, '%Y%m%d').strftime("%Y-%m-%d")
        work = db.session.execute(
            db.select(Work).filter(sql.func.date(Work.startDate) <= sql.func.date(workDate)).filter(sql.func.date(Work.endDate) >= sql.func.date(workDate))
        ).scalar()
        return work_schema.dump(work)

api.add_resource(WorkListAll, "/api/work")
api.add_resource(WorkFilterID, "/api/work/<int:workID>")
api.add_resource(WorkFilterDate, "/api/work/date/<string:date>")


@app.route("/")
def home():
    return 


if __name__ == "__main__":
    app.run(debug = True)

