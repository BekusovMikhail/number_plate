posgres_DB = "plate_detection_db"
posgres_user = "plate_detection_user"
posgres_user_password = "lprpassword"
sql_alchemy_engine = f"postgresql+psycopg2://{posgres_user}:{posgres_user_password}@127.0.0.1/{posgres_DB}"

add_image_row_sql = "INSERT INTO images (image_before_treatment, image_after_treatment) VALUES ('{}', '{}');"

add_car_box_row_sql = "INSERT INTO car (x1, y1, x2, y2, score, type, fk_image_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"

add_lp_box_row_sql = "INSERT INTO license_plate (x1, y1, x2, y2, score, text, type, fk_car_id) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"

sqlCreateDatabase = """CREATE DATABASE {}
                            WITH
                            OWNER = {}
                            ENCODING = 'UTF8'
                            CONNECTION LIMIT = -1
                            IS_TEMPLATE = False;"""

sqlDropDatabase = "DROP DATABASE {};"

sql_delete_images_where = "delete from images where {} = '{}';"

# sql_select_images_where = "select * from images where {} = '{}';"

# sql_select_car_boxes_where = "select * from car where {} = '{}';"

# sql_select_lp_where = "select * from license_plate where {} = '{}';"

# create_tables_sql = """
#                         CREATE TABLE images
#                         (
#                             image_id SERIAL PRIMARY KEY,
#                             image_before_treatment varchar,
#                             image_after_treatment varchar);

#                         ALTER TABLE IF EXISTS images
#                             OWNER to plate_detection_user;
                            
#                         CREATE TABLE car (
#                             car_id SERIAL PRIMARY KEY,
#                             x1 int,
#                             x2 int,
#                             y1 int,
#                             y2 int,
#                             score float,
#                             type varchar,
#                             fk_image_id integer REFERENCES images (image_id) ON DELETE CASCADE

#                         );
#                         ALTER TABLE IF EXISTS car_bbox
#                             OWNER to plate_detection_user;

#                         CREATE TABLE license_plate (
#                             lp_id SERIAL PRIMARY KEY,
#                             x1 int,
#                             x2 int,
#                             y1 int,
#                             y2 int,
#                             score float,
#                             text varchar,
#                             type varchar,
#                             fk_car_id integer REFERENCES car (car_id) ON DELETE CASCADE
#                         );
#                         ALTER TABLE IF EXISTS license_plate
#                             OWNER to plate_detection_user
#                     """
