#!/usr/bin/env python
# coding=utf-8
from datetime import date, datetime
import psycopg2


def calculate_age(birthdate):
    b_date_obj = datetime.strptime(birthdate,'%m/%d/%Y')
    age = (datetime.today() - b_date_obj).days/365
    return age


def calculate_rate(zipcode, age):
    rate = calculate_base_rate(zipcode, age);
    return rate

def connect_to_db():
    try:
        conn = psycopg2.connect("dbname='ratesetter' user='postgres'")
    except:
        print "I am unable to connect to the database"
    return conn

def calculate_base_rate(zipcode, age):
    #Conect to database
    if age < 20:
        age =20

    if age > 65:
        age = 65

    conn = connect_to_db()

    cur = conn.cursor()

    cur.execute("SELECT premiumrate from mapping2 m2,mapping1 m1 \
    where m2.age = %(_age)s and m1.zipcode = %(_zip)s and m1.statecode = m2.statecode \
    and m2.ratingarea = m1.ratingarea LIMIT 1", {'_age' : age, '_zip':zipcode})

    row = cur.fetchone()
    if(row is not None):
        base_rate = row[0]
    else:
        if age < 40:
            base_rate = 197.62
        else:
            base_rate = 221.37
    return base_rate

def get_plan_name(plan_code):
    return {
        'AHIP': ['Platinum Perfection', 15],
        'AHIG': ['Golden Protection', 10] ,
        'AHIS': ['Silver Lining', 5],
        'AHIB': ['Bronze Shield', 0]
    }[plan_code]

def get_income_addition(income_class):
    return {
        'class1': 0,
        'class2': 5 ,
        'class3': 15
    }[income_class]
