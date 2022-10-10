#!/usr/bin/env python3

"""
SQL
DB: piNet
Purpose:  Experiment with data structure, table structure and use prepared statements.
"""

import mysql.connector
from mysql.connector import Error
import piNetDate

# get from config later
host = ""
port = 3306
user = ""
passwd = ""
db = "pinet_sensors"


def connect_db(db=db):
    # get db config
    conn = None
    try:
        conn = mysql.connector.connect(user=user, password=passwd,
                                       host=host,
                                       port=port,
                                       database=db)

        if conn.is_connected():
            return conn
        else:
            return False

    except Error as error:
        return (error)


def write_sensor_value(sensor_id, value):
    cnx = connect_db(db)
    cursor = cnx.cursor()
    sql = "INSERT INTO sensor_readings (id, sensor_id, timestamp, value) VALUES (NULL, %s, NOW(), %s)"
    val = (sensor_id, value)
    cursor.execute(sql, val)
    cnx.commit()


def get_locations():
    """
        return:  list of dictionaries
            [
                {'id': 1, 'name': 'polyhub', 'location': 'Poly Tunnel'},
                {'id': 2, 'name': 'TEST', 'location': 'test location'}
            ]
    """
    cnx = connect_db(db)
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * FROM sensor_locations"
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows


def get_location(sensor_id):
    # return: dictionary of fields
    cnx = connect_db(db)
    cursor = cnx.cursor(dictionary=True)

    sql = ("SELECT * FROM sensor_locations WHERE location_id='{}'".format(sensor_id))

    # count = cursor.rowcount
    cursor.execute(sql)
    row = cursor.fetchone()
    # return type(row)
    return row


def get_sensor_list():
    """
        return:  list of dictionaries
            [
                {'id': 1, 'name': 'polyhub', 'location': 'Poly Tunnel'},
                {'id': 2, 'name': 'TEST', 'location': 'test location'}
            ]
    """
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * FROM sensors"
    cursor.execute(sql)
    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows

def get_sensor_latest_dict(sensor_id):

    sql = "SELECT * FROM sensor_readings WHERE sensor_id='{}' ORDER BY id DESC LIMIT 1".format(
        sensor_id)
    pass

def get_sensor_latest(sensor_id):
    """
        return:  dictionary
            {'id': 5, 'sensor_id': 3, 'timestamp': datetime.datetime(2020, 6, 19, 21, 24, 44), 'value': 999.99}
    """
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)
    sql = "SELECT * FROM sensor_readings WHERE sensor_id='{}' ORDER BY id DESC LIMIT 1".format(
        sensor_id)
    cursor.execute(sql)
    rows = cursor.fetchone()
    cursor.close()
    cnx.close()
    return rows


if __name__ == "__main__":

    try:
        # cnx = connect_db("pinet_sensors")
        # print(cnx)
        locs = get_locations()
        for loc in locs:
            print(f"{loc['location_id']} - {loc['name']} -- {loc['location']}")

        sensor_l = get_sensor_list()
        print(type(sensor_l))

        for sensor in sensor_l:
            print(f"{sensor['sensor_id']} is {sensor['name']}")

        latest_3 = {}
        latest_3 = get_sensor_latest(3)
        latest_3['location']
        # print(latest_3)
        ts = str(latest_3['timestamp'])
        print(
            f"ID:{latest_3['sensor_id']}Time: {piNetDate.dateStr2Ts(ts)} Value:{latest_3['value']}")

        write_sensor_value(3, 20.00)

    finally:
        pass
    #     if cnx is not None and cnx.is_connected():
    #         cnx.close()
    #         print("Connection closed.")
