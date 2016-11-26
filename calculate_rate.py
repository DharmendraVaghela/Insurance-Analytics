#!/usr/bin/env python
# coding=utf-8

import psycopg2

def calculate_rate(zipcode, age):
    rate = calculate_base_rate(zipcode, age);
    return rate


def calculate_base_rate(zipcode, age):
    try:
        conn = psycopg2.connect("dbname='ratesetter' user='postgres'")

        cur = conn.cursor()

        cur.execute("SELECT rate from base_rate;")

        row = cur.fetchone()

        return row[0]
    except:
        print "I am unable to connect to the database"
