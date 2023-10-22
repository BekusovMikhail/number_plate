import psycopg2

from .postgre_config import *
import json
import time
import os
import cv2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()

    bp = os.path.join(os.getcwd(), images_before_treatment, image_name)
    ap = os.path.join(os.getcwd(), images_after_treatment, image_name)

    cv2.imwrite(bp, image_np)
    cursor.execute(sql_delete_images_where.format("image_before_treatment", bp))
    cursor.execute(add_image_row_sql.format(bp, ap))

    cursor.execute(sql_select_images_where.format("image_before_treatment", bp))
    return cursor.fetchall()


def add_car_sql(boxes, scores, types, image_id):
    con = psycopg2.connect(
        dbname=posgres_DB,
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    assert len(boxes) == len(scores)
    assert len(boxes) == len(types)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()

    for i in range(len(boxes)):
        cursor.execute(
            add_car_box_row_sql.format(
                boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3], scores[i], types[i], image_id
            )
        )
    cursor.execute(sql_select_car_boxes_where.format("fk_image_id", image_id))
    return cursor.fetchall()


def add_lp_sql(boxes, scores, types, texts, car_id):
    con = psycopg2.connect(
        dbname=posgres_DB,
        user=posgres_user,
        password=posgres_user_password,
        host="localhost",
        port="5432",
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    assert len(boxes) == len(scores)
    assert len(boxes) == len(types)

    for i in range(len(boxes)):
        cursor.execute(
            add_lp_box_row_sql.format(
                boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3], scores[i], texts[i], types[i], car_id
            )
        )
    cursor.execute(sql_select_lp_where.format("fk_car_id", car_id))
    return cursor.fetchall()


def create_db():
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
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()

    cursor.execute(create_tables_sql)


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
