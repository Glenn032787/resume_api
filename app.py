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
        startYear = request.json['startYear']
        startMonth = request.json['startMonth']
        startDay = request.json['startDay']
        startDate = datetime(startYear, startMonth, startDay)

        endYear = request.json['startYear']
        endMonth = request.json['endMonth']
        endDay = request.json['endDay']
        endDate = datetime(endYear, endMonth, endDay)


        newSchool = Education(
            university = request.json['university'],
            location = request.json['location'],
            degree = request.json['degree'],
            startDate = startDate,
            endDate = endDate,
            gpa = request.json['gpa']
        )

        db.session.add(newSchool)
        db.session.commit()
        return education_schema.dump(newSchool)
    
class EducationFilterID(Resource):
    def get(self, educationID):
        school = Education.query.get_or_404(educationID)
        return education_schema.dump(school)

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


api.add_resource(EducationListAll, 'api/education')
api.add_resource(EducationFilterID, 'api/education/<int:educationID>')
api.add_resource(EducationFilterLocation, 'api/education/location/<string:location>')
api.add_resource(EducationFilterDate, 'api/education/date/<string:date>')


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

class EmailFilterType(Resource):
    def get(self, emailType):
        email = db.session.execute(
            db.select(Email).filter(Email.emailType == emailType)
        ).scalar()

        return email_schema.dump(email)

api.add_resource(EmailListAll, 'api/email')
api.add_resource(EmailFilterID, 'api/email/<int:emailId>')
api.add_resource(EmailFilterType, 'api/email/<string:emailType>')

## Link
class linkListAll(Resource):
    def get(self):
        links = Link.query.all()
        return link_multischema.dump(links)



@app.route("/")
def home():
    return 


if __name__ == "__main__":
    app.run(debug = True)