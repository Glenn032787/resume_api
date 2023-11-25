from flask import Flask, request 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields
from datetime import datetime
from model import *
from database import app, db, ma
from sqlalchemy import sql
from apispec import APISpec
from flask_apispec.views import MethodResource
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import doc, use_kwargs, marshal_with
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow



api = Api(app)
apiSpec = APISpec(
        title='Glenn Resume API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    )
##### DOCUMENTATION (using swasgger)
app.config.update({
    'APISPEC_SPEC': apiSpec,
    'APISPEC_SWAGGER_URL': '/api/doc/json/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/api/doc/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)
# Tag info
apiSpec.tag({'name': 'Education', 'description': 'Api endpoint for academic history'})
apiSpec.tag({'name': 'Email', 'description': 'Api endpoint to get emails'})
apiSpec.tag({'name': 'Transcript', 'description': 'Api endpoint for transcript'})
apiSpec.tag({'name': 'Link', 'description': 'Api endpoint for links and socials'})
apiSpec.tag({'name': 'Publication', 'description': 'Api endpoint for all publication and academic papers'})
apiSpec.tag({'name': 'Work', 'description': 'Api endpoint for all professional work experiences'})


### Education
class EducationListAll(MethodResource, Resource):
    @doc(
        description="### Output all education data in resume", 
        summary='Get all education date', 
        tags=['Education']
    )
    @marshal_with(
        EducationResponseSchema(many=True), 
        description="Success", 
        code = 200)
    def get(self):
        schools = Education.query.all()
        return education_multischema.dump(schools)

    @doc(
        description="### Create a new education entry in resume", 
        summary='Create education entry', 
        tags=['Education'],
    )
    @use_kwargs(
        {
            "university": fields.Str(),
            "location": fields.Str(),
            "degree": fields.Str(),
            "startDate": fields.Date(format = '%Y-%m-%d'),
            "endDate": fields.Date(format = "%Y-%m-%d"),
            "gpa": fields.Integer(),
        }, location=('json'))
    @marshal_with(
        EducationResponseSchema(), 
        code = 200, 
        description="Successfully added new Education object")
    def post(self, **kwargs):
        newSchool = Education(
            university = request.json['university'],
            location = request.json['location'],
            degree = request.json['degree'],
            startDate = sql.func.date(request.json["startDate"]),
            endDate = sql.func.date(request.json["endDate"]),
            gpa = request.json['gpa']
        )

        db.session.add(newSchool)
        db.session.commit()
        return education_schema.dump(newSchool), 200

class EducationFilterID(MethodResource, Resource):
    @doc(
        description='### Filter Education data based on Education ID', 
        summary = 'Get education using ID', 
        tags=['Education'],
        params={'educationID': 
            {
                'description': 'The ID for the education entry'
            }
        }
    )
    @marshal_with(
        EducationResponseSchema(), 
        description="Success", 
        code = 200)
    def get(self, educationID):
        school = Education.query.get_or_404(educationID)
        return education_schema.dump(school), 200
    
    @doc(
        description='### Delete education date based on ID', 
        summary = 'Delete education entry', 
        tags=['Education'],
        params={'educationID': 
            {
                'description': 'The ID for the education entry'
            }
        }
    )
    @marshal_with( 
        ma.SQLAlchemyAutoSchema(),
        description="Successfully deleted education object", 
        code = 204)
    def delete(self, educationID):
        school = Education.query.get_or_404(educationID)
        db.session.delete(school)
        db.session.commit()
        return '', 204

class EducationFilterLocation(MethodResource, Resource):
    @doc(
        description='### Get education date based on location', 
        summary ="Filter education with location", 
        tags=['Education'],
        params={'location': 
            {
                'description': 'Location of school'
            }
        }
    )
    @marshal_with(
        EducationResponseSchema(), 
        description="Success", 
        code = 200)
    def get(self, location):
        school = db.session.execute(
            db.select(Education).filter_by(location = location)
        ).scalars()
        return education_multischema.dump(school), 200

class EducationFilterDate(MethodResource, Resource):
    @doc(
        description='### Return the school where enrollment occurred on the specified date.',
        params={'date': 
            {
                'description': 'Date of entrollment (format: YYYYMMDD)',
                'example': '20220402'
            }
        },
        summary='Filter education with date',
        tags=['Education']
    )
    @marshal_with(
        EducationResponseSchema(), 
        description="Success", 
        code = 200)
    def get(self, date):
        date = datetime.strptime(date, '%Y%m%d').strftime("%Y-%m-%d")
        school = db.session.execute(
            db.select(Education).filter(sql.func.date(Education.startDate) <= sql.func.date(date)).filter(sql.func.date(Education.endDate) >= sql.func.date(date))
        ).scalar()
        return education_schema.dump(school), 200


api.add_resource(EducationListAll, '/api/education')
api.add_resource(EducationFilterID, '/api/education/<int:educationID>')
api.add_resource(EducationFilterLocation, '/api/education/location/<string:location>')
api.add_resource(EducationFilterDate, '/api/education/date/<string:date>')
docs.register(EducationListAll)
docs.register(EducationFilterID)
docs.register(EducationFilterLocation)
docs.register(EducationFilterDate)


## Email
class EmailListAll(MethodResource, Resource):
    @doc(
        description='### Output all email data in resume', 
        summary="Get all email data",
        tags=['Email']
    )
    @marshal_with(
        EmailSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self):
        emails = Email.query.all()
        return email_multischema.dump(emails)



    @doc(
        description='### Create new email entry', 
        summary = "Create new email entry",
        tags=['Email']
    )
    @marshal_with(
        EmailSchema(), 
        description="Success", 
        code = 200)
    @use_kwargs(
        {
            'emailType': fields.String(required = True), 
            'email': fields.Email(required = True),
            'id': fields.Integer()
        }, 
        location=('json'),
        description = "Email object that needs to be added to the resume"
        )
    def post(self, **kwargs):
        newEmail = Email(
            emailType = request.json['emailType'],
            email = request.json['email']
        )
        db.session.add(newEmail)
        db.session.commit()
        return email_schema.dump(newEmail)

class EmailFilterID(MethodResource, Resource):
    @doc(
        description='### Filter email data based on Education ID', 
        summary = "Get email using ID",
        tags=['Email'],
        params={'emailID': 
            {
                'description': 'The ID for the email entry'
            }
        }
    )
    @marshal_with(
        EmailSchema(), 
        description="Success", 
        code = 200)
    def get(self, emailId):
        email = Email.query.get_or_404(emailId)
        return email_schema.dump(email), 200
    
    @doc(
        description='### Delete email date based on ID', 
        summary = "Delete email entry",
        tags=['Email'],
        params={'emailID': 
            {
                'description': 'The ID for the email entry'
            }
        }
    )
    @marshal_with(
        ma.SQLAlchemyAutoSchema, 
        description="Successfully delete entry", 
        code = 204)
    def delete(self, emailId):
        email = Email.query.get_or_404(emailId)
        db.session.delete(email)
        db.session.commit()
        return '', 204

class EmailFilterType(MethodResource, Resource):
    @doc(
        description='### Filter email data based on email type', 
        summary = "Get email using email type",
        tags=['Email'],
        params={'emailType': 
            {
                'description': 'Type of email',
                'example': 'Personal'
            }
        }
    )
    @marshal_with(
        EmailSchema(), 
        description="Success", 
        code = 200)
    def get(self, emailType):
        email = db.session.execute(
            db.select(Email).filter(Email.emailType == emailType)
        ).scalar()

        return email_schema.dump(email), 200

api.add_resource(EmailListAll, '/api/email')
api.add_resource(EmailFilterID, '/api/email/<int:emailId>')
api.add_resource(EmailFilterType, '/api/email/<string:emailType>')
docs.register(EmailListAll)
docs.register(EmailFilterID)
docs.register(EmailFilterType)


## Link
class LinkListAll(MethodResource, Resource):
    @doc(
        description='### Output all link data in resume', 
        summary="Get all link data",
        tags=['Link']
    )
    @marshal_with(
        LinkSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self):
        links = Link.query.all()
        return link_multischema.dump(links), 200
    
    @doc(
        description='### Create new link entry', 
        summary="Create new link entry",
        tags=['Link']
    )
    @marshal_with(
        LinkSchema(), 
        description="Success", 
        code = 200)
    @use_kwargs(
        {
            'linkType': fields.String(required = True), 
            'link': fields.URL(required = True, relative = True, require_tld = True, example="http://example.com")
        }, 
        location=('json'),
        description = "Link object that needs to be added to the resume"
    )
    def post(self, linkType, link):
        newLink = Link(
            linkType = request.json['linkType'],
            link = request.json['link']
        )

        db.session.add(newLink)
        db.session.commit()
        return link_schema.dump(newLink), 200        

class LinkFilterId(MethodResource, Resource):
    @doc(
        description='### Filter link data based on link ID', 
        summary="Get link using ID",
        tags=['Link'],
        params={'LinkID': 
            {
                'description': 'The ID for the link entry'
            }
        }
    )
    @marshal_with(
        LinkSchema(), 
        description="Success", 
        code = 200)
    def get(self, LinkId):
        link = Link.query.get_or_404(LinkId)
        return link_schema(link), 200
    
    @doc(
        description='### Delete link data based on link ID', 
        summary="Delete link entry",
        tags=['Link'],
        params={'LinkID': 
            {
                'description': 'The ID for the link entry'
            }
        }
    )
    @marshal_with(
        ma.SQLAlchemyAutoSchema(), 
        description="Success", 
        code = 200)
    def delete(self, LinkId):
        link = Link.query.get_or_404(LinkId)
        db.session.delete(link)
        db.session.commit()
        return '', 204

class LinkFilterType(MethodResource, Resource):
    @doc(
        description='### Filer link data based on link type', 
        summary="Filter by link type",
        tags=['Link'],
        params={'linkType': 
            {
                'description': 'The name of the link',
                'default': "github"
            }
        }
    )
    @marshal_with(
        LinkSchema(), 
        description="Success", 
        code = 200)
    def get(self, linkType):
        link = db.session.execute(
            db.select(Link).filter(Link.linkType == linkType)
        ).scalar()
        return link_schema.dump(link), 200

api.add_resource(LinkListAll, "/api/link")
api.add_resource(LinkFilterId, "/api/link/<int:LinkId>")
api.add_resource(LinkFilterType, "/api/link/<string:linkType>")
docs.register(LinkListAll)
docs.register(LinkFilterId)
docs.register(LinkFilterType)

# Transcript
class TranscriptListAll(MethodResource, Resource):
    @doc(
        description='### Output all link transcript in resume', 
        summary="Get all transcript data",
        tags=['Transcript']
    )
    @marshal_with(
        TranscriptSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self):
        transcripts = Transcript.query.all()
        return transcript_multischema.dump(transcripts)
    
    @doc(
        description='### Create new transcript entry', 
        summary="Create new transcript entry",
        tags=['Transcript']
    )
    @marshal_with(
        TranscriptSchema(), 
        description="Success", 
        code = 200)
    @use_kwargs(
        {
            'school': fields.Number(required = True), 
            'courseCode': fields.String(required = True),
            'courseTitle': fields.String(required = True), 
            'grade': fields.Number(required = True), 
            'semester': fields.Number(required = True)
        }, 
        location=('json'),
        description = "Link object that needs to be added to the resume"
    )
    def post(self, **kwargs):
        newTranscript = Transcript(
            school = request.json['school'],
            courseCode = request.json['courseCode'],
            courseTitle = request.json['courseTitle'],
            grade = request.json['grade'],
            semester = request.json['semester']
        )
        db.session.add(newTranscript)
        db.session.commit()
        return transcript_schema.dump(newTranscript)    
    
class TranscriptFilterId(MethodResource, Resource):
    @doc(
        description='### Filter based on transcript ID', 
        summary="Get transcript using ID",
        tags=['Transcript'],
        params={'transcriptID': 
            {
                'description': 'The ID for the transcript entry'
            }
        }
    )
    @marshal_with(
        TranscriptSchema(), 
        description="Success", 
        code = 200)
    def get(self, transcriptID):
        transcript = Transcript.query.get_or_404(transcriptID)
        return transcript_schema.dump(transcript)
    
    @doc(
        description='### Delete transcript data based on transcript ID', 
        summary="Delete transcript entry",
        tags=['Transcript'],
        params={'transcriptID': 
            {
                'description': 'The ID for the transcript entry'
            }
        }
    )
    @marshal_with(
        ma.SQLAlchemyAutoSchema(),
        description="Success", 
        code = 200)
    def delete(self, transcriptID):
        transcript = Transcript.query.get_or_404(transcriptID)
        db.session.delete(transcript)
        db.session.commit()
        return '', 204

class TranscriptFilterSchool(MethodResource, Resource):
    @doc(
        description='### Filter transcripts based on school ID', 
        summary="Get transcript from specific school",
        tags=['Transcript'],
        params={'schoolID': 
            {
                'description': 'The foreign key for the school ID'
            }
        }
    )
    @marshal_with(
        TranscriptSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self, schoolID):
        transcripts = db.session.execute(
            db.select(Transcript).filter(Transcript.school == schoolID)
        ).scalars()

        return transcript_multischema.dump(transcripts)

class TranscriptFilterSchoolSemester(MethodResource, Resource):
    @doc(
        description='### Filter transcripts based on school ID and semester number', 
        summary="Get transcript from specific school and semseter",
        tags=['Transcript'],
        params={'schoolID': 
            {
                'description': 'The foreign key for the school ID'
            },
            "semester":  
            {
                'description': 'The semester number for that school'
            }
        }
    )
    @marshal_with(
        TranscriptSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self, schoolID, semester):
        transcripts = db.session.execute(
            db.select(Transcript).filter(Transcript.school == schoolID).filter(Transcript.semester == semester)
        ).scalars()
        return transcript_multischema.dump(transcripts)

class TranscriptFilterCourseCode(MethodResource, Resource):
    @doc(
        description='### Filter transcripts based on course code', 
        summary="Get transcript for specific course",
        tags=['Transcript'],
        params={'courseCode': 
            {
                'description': 'Course code for that course'
            }
        }
    )
    @marshal_with(
        TranscriptSchema(), 
        description="Success", 
        code = 200)
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
docs.register(TranscriptListAll)
docs.register(TranscriptFilterId)
docs.register(TranscriptFilterSchool)
docs.register(TranscriptFilterSchoolSemester)
docs.register(TranscriptFilterCourseCode)

# Publication
class PublicationListAll(MethodResource, Resource):
    @doc(
        description='### Output all publication data in resume', 
        summary="Get all publication data",
        tags=['Publication']
    )
    @marshal_with(
        PublicationSchema(many = True), 
        description="Success", 
        code = 200)
    def get(self):
        publications = Publication.query.all()
        return publication_multischema.dump(publications)

    @doc(
        description='### Create new publication entry', 
        summary="Create new publication entry",
        tags=['Publication']
    )
    @marshal_with(
        PublicationSchema(), 
        description="Success", 
        code = 200)
    @use_kwargs(
        {
            'title': fields.String(required = True), 
            'journal': fields.String(required = True), 
            'doi': fields.URL(required = True, example = "https://doi.org"), 
            'status': fields.String(required = True), 
            'date': fields.Date(format="%Y-%m-%d", required = True), 
        }, 
        location=('json'),
        description = "Publication object that needs to be added to the resume"
    )
    def post(self, **kwargs):
        newPublication = Publication(
            title = request.json['title'],
            journal = request.json['journal'],
            doi = request.json['doi'],
            date = sql.func.date(request.json['date']) ,
            status = request.json['status'],
        )

        db.session.add(newPublication)
        db.commit()
        return publication_schema.dump(newPublication)

class PublicationFilterID(MethodResource, Resource):
    @doc(
        description='### Filter publication data based on ID', 
        summary="Get publication using ID",
        tags=['Publication'], 
        params={'publcationID': 
            {
                'description': 'The ID for the publication object'
            }
        }
    )
    @marshal_with(
        PublicationSchema(), 
        description="Success", 
        code = 200)
    def get(self, publicationID):
        publication = Publication.query.get_or_404(publicationID)
        return publication_schema.dump(publication)

    @doc(
        description='### Delete publication with ID', 
        summary="Delete publication with ID",
        tags=['Publication'], 
        params={'publcationID': 
            {
                'description': 'The ID for the publication object'
            }
        }
    )
    @marshal_with(
        ma.SQLAlchemyAutoSchema(), 
        description="Success", 
        code = 200)
    def delete(self, publicationID):
        publication = Publication.query.get_or_404(publicationID)
        db.session.delete(publication)
        db.commit()
        return '', 204

class PublicationFilterStatus(MethodResource, Resource):
    @doc(
        description='### Filter publication based on publication status', 
        summary="Filter publication with status",
        tags=['Publication'], 
        params={'status': 
            {
                'description': 'The status of publcation (published, preprint& draft)'
            }
        }
    )
    @marshal_with(
        PublicationSchema(many = True),
        description="Success", 
        code = 200)
    def get(self, status):
        publications = db.session.execute(
            db.select(Publication).filter(Publication.status == status)
        ).scalars()

        return publication_multischema.dump(publications)

api.add_resource(PublicationListAll, "/api/publication")
api.add_resource(PublicationFilterID, "/api/publication/<int:publicationID>")
api.add_resource(PublicationFilterStatus, "/api/publication/<string:status>")
docs.register(PublicationListAll)
docs.register(PublicationFilterID)
docs.register(PublicationFilterStatus)

# Work
class WorkListAll(MethodResource, Resource):
    @doc(
        tags=['Work'],
        description = '### Output all work experience data in resume', 
        summary="Get all work experience",
    )
    @marshal_with(WorkSchema(many=True), description="Success", code = 200)
    def get(self):
        work = Work.query.all()
        return work_multischema.dump(work), 200

    @doc(
        tags=['Work'],
        description = '### Create new work experience entry', 
        summary="Create new work experience entry",
    )
    @marshal_with(WorkSchema(), description="Success", code = 200)
    @use_kwargs(
        {
            'jobTitle': fields.String(required = True), 
            'company': fields.String(required = True), 
            'location': fields.String(required = True), 
            'startDate': fields.Date(format="%Y-%m-%d", required = True), 
            'endDate': fields.Date(format="%Y-%m-%d", required = True),
            'id': fields.Integer(required = False)
        },
        location=('json'),
        description = "Work experience object that needs to be added to the resume"
    )
    def post(self, **kwargs):
        newWork = Work(
            jobTitle = request.json["jobTitle"],
            company = request.json["company"],
            location = request.json["location"],
            startDate = sql.func.date(request.json["startDate"]),
            endDate = sql.func.date(request.json["endDate"])
        )
        db.session.add(newWork)
        db.session.commit()
        return work_schema.dump(newWork)

class WorkFilterID(MethodResource, Resource):
    @doc(
        description='### Filter work experience with ID', 
        summary="Filter work experience with ID",
        tags=['Work'], 
        params={'workID': 
            {
                'description': 'The ID for the work experience object'
            }
        }
    )
    @marshal_with(
        WorkSchema(), 
        description="Success", 
        code = 200)
    def get(self, workID):
        work = Work.query.get_or_404(workID)
        return work_schema.dump(work)
    
    @doc(
        description='### Delete work experience with ID', 
        summary="Delete work experience",
        tags=['Work'], 
        params={'workID': 
            {
                'description': 'The ID for the work experience object'
            }
        }
    )
    @marshal_with(
        ma.SQLAlchemyAutoSchema(), 
        description="Succesfully deleted", 
        code = 204)
    def delete(self, workID):
        work = Work.query.get_or_404(workID)
        db.session.delete(work)
        db.session.commit()
        return '', 204

class WorkFilterDate(MethodResource, Resource):
    @doc(
        description='### Filer the work experience held based on the provided date', 
        summary="Filter work experience based on date",
        tags=['Work'], 
        params={'date': 
            {
                'description': 'The date in YYYYMMDD format'
            }
        }
    )
    @marshal_with(
        WorkSchema(), 
        description="Success", 
        code = 200)
    def get(self, date):
        workDate = datetime.strptime(date, '%Y%m%d').strftime("%Y-%m-%d")
        work = db.session.execute(
            db.select(Work).filter(sql.func.date(Work.startDate) <= sql.func.date(workDate)).filter(sql.func.date(Work.endDate) >= sql.func.date(workDate))
        ).scalar()
        return work_schema.dump(work)

api.add_resource(WorkListAll, "/api/work")
api.add_resource(WorkFilterID, "/api/work/<int:workID>")
api.add_resource(WorkFilterDate, "/api/work/date/<string:date>")
docs.register(WorkListAll)
docs.register(WorkFilterID)
docs.register(WorkFilterDate)

@app.route("/")
def home():
    return 




if __name__ == "__main__":
    app.run(debug = True)

