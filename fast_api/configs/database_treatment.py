import psycopg2

from .postgre_config import *
import json
import time
import os
import cv2

images_before_treatment = "images_before_treatment"
images_after_treatment = "images_after_treatment"


def add_image_sql(image_np, image_name):
    con = psycopg2.connect(
        dbname=posgres_DB,
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    cursor = con.cursor()
    print(con.info.status)
    print(cursor.execute("select * from images"))
    # print(cursor.fetchall())
    bp = os.path.join(os.getcwd(), images_before_treatment, image_name)
    ap = os.path.join(os.getcwd(), images_after_treatment, image_name)

    cv2.imwrite(bp, image_np)

    # cursor.execute(add_image_row_sql.format(bp, ap))


def create_db():
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    con = psycopg2.connect(
        dbname="postgres",
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()

    cursor.execute(sqlCreateDatabase.format(posgres_DB, posgres_user))

    con = psycopg2.connect(
        dbname=posgres_DB,
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    cursor = con.cursor()

    cursor.execute(create_tables_sql)
    print(
        cursor.execute(
            "INSERT INTO images (image_before_treatment, image_after_treatment) VALUES ('/home/tmp', '/home/tmp');"
        )
    )
    print(cursor.execute("select * from images"))
    print(cursor.fetchall())
    print(con.info.dbname)
    # cursor.execute(create_image_table)
    # cursor.execute(create_car_table)
    # cursor.execute(create_lp_table)


def drop_db():
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    con = psycopg2.connect(
        dbname="postgres",
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    name_Database = posgres_DB

    sqlDropDatabase = f"DROP DATABASE {name_Database};"

    cursor.execute(sqlDropDatabase.format(name_Database))


def get_db_user_credentials():
    return {
        "posgres_user": posgres_user,
        "posgres_user_password": posgres_user_password,
        "command": f"sudo -u postgres createuser --login --no-superuser --createdb --createrole -e {posgres_user} -P;",
    }
