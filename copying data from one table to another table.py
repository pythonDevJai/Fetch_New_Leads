
# Library Imports
import json     # This lib used for converting Python objects to JSON objects
from datetime import datetime
import psycopg2 # For connecting to the database
from flask import Flask # To create application object
from flask import request # To read the request details like parameters/request body
from flask_restful import Api
from sqlalchemy import Column, String, Integer, Date, BOOLEAN, and_, or_

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
# Disable session pooling from sqlalchemy side use only postgres pool
from flask import jsonify
import os
from datetime import date

# Create the application object using flask framework
app = Flask(__name__)

# Parse the app instance/object to Api Base class to utilise all the services
api = Api(app)

# This a the base class which should have all database table related features
# To work with any database table operations

Base = declarative_base()

# Construct the database URL which will be used for connecting to right database
database_url = "postgresql://postgres:1526@localhost:5432/postgres"

# poolclass=NullPool - Disable sqlalchemy poolling using NullPool
# as by default Postgres has its own pool

# database_url - Constructed url to create engine object which will then
# be used to perform database operations.

# echo - To capture all database events echo set to True which will give more insights about the
# database operations which will eventually help us to understand what's going on while app
# is being using by the end users (customers)
engine = create_engine(database_url, echo=True, poolclass=NullPool)

# Enabling the engine object , get connceted to the database
conn = engine.connect()

# Create session using sessio maker
Session = sessionmaker(bind=engine)

# Create the session object -This is the object being used in the all data base transactions!
session = Session()


class ProductEnquiry(Base):
    """ Product enquiry form model which has all details -table names & columns"""
    __tablename__ = "productenquiry"
    customerName = Column("customer_name", String)
    dealerName = Column("dealer_name" , String)
    createdDate = Column("created_date", String)
    mobileNumber = Column("mob_no", Integer, primary_key=True)
    email = Column("email", String)
    vehicleModel = Column("vehicle_model",String)
    state = Column("state",String)
    district = Column("district",String)
    city = Column("city",String)
    existingVehicle = Column("existing_vehicle",String)
    wantTestDrive = Column("want_to_take_a_test_ride", BOOLEAN)
    dealerState = Column("dealer_state",String)
    dealerTown = Column("dealer_town",String)
    dealerCode = Column("dealer_code" , String)
    briefAboutEnquery = Column("brief_about_enquiry", String)
    expectedDateOfPurchase = Column("expected_date_of_purchase", String)
    intendedUsage = Column("intended_usage", String)
    age = Column("age" , Integer)
    gender = Column("gender" , String)
    occupation = Column("occupation" , String)
    isNew = Column("is_new" , BOOLEAN)
    feedBack = Column("feed_back" , String)
    sentToDealer = Column("sent_to_dealer" , BOOLEAN)


class CompanyPortal(Base):
    """ Product enquiry form model which has all details -table names & columns"""
    __tablename__ = "company_portal"
    customerName = Column("customer_name", String)
    dealerName = Column("dealer_name" , String)
    createdDate = Column("created_date", String)
    mobileNumber = Column("mob_no", Integer, primary_key=True)
    email = Column("email", String)
    vehicleModel = Column("vehicle_model",String)
    state = Column("state",String)
    district = Column("district",String)
    city = Column("city",String)
    existingVehicle = Column("existing_vehicle",String)
    wantTestDrive = Column("want_to_take_a_test_ride", BOOLEAN)
    dealerState = Column("dealer_state",String)
    dealerTown = Column("dealer_town",String)
    dealerCode = Column("dealer_code" , String)
    briefAboutEnquery = Column("brief_about_enquiry", String)
    expectedDateOfPurchase = Column("expected_date_of_purchase", String)
    intendedUsage = Column("intended_usage", String)
    age = Column("age" , Integer)
    gender = Column("gender" , String)
    occupation = Column("occupation" , String)
    isNew = Column("is_new" , BOOLEAN)
    feedBack = Column("feed_back" , String)
    sentToDealer = Column("sent_to_dealer" , BOOLEAN)
    isNewCustomer = Column("is_new_customer" , BOOLEAN)


@app.route('/update-customer', methods=['PATCH'])
def update_customer_info():

    mobile= request.args.get('mobile')
    result = session.query(ProductEnquiry).filter(ProductEnquiry.mobileNumber == mobile , ProductEnquiry.sentToDealer == False)\
                                          .update({'sentToDealer' : True})
    session.commit()
    set_customer_status(mobile)

    return "Record Updated Successfully"

def set_customer_status(mobile):
    name = session.query(ProductEnquiry.customerName).filter(ProductEnquiry.mobileNumber == mobile).all()
    session.query(CompanyPortal).filter(CompanyPortal.customerName == name[0][0])\
                                .update({'isNewCustomer':False})
    session.commit()


app.run(debug = False)
