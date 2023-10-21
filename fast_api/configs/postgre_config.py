posgres_DB = "plate_detection_db"
posgres_user = "plate_detection_user"
posgres_user_password = "lprpassword"

add_image_row_sql = "INSERT INTO images (image_before_treatment, image_after_treatment) VALUES ('{}', '{}');"


sqlCreateDatabase = """CREATE DATABASE {}
                            WITH
                            OWNER = {}
                            ENCODING = 'UTF8'
                            CONNECTION LIMIT = -1
                            IS_TEMPLATE = False;"""

sqlDropDatabase = "DROP DATABASE {};"

create_tables_sql = """
                        CREATE TABLE images
                        (
                            image_id SERIAL PRIMARY KEY,
                            image_before_treatment varchar,
                            image_after_treatment varchar);

                        ALTER TABLE IF EXISTS images
                            OWNER to plate_detection_user;
                            
                        CREATE TABLE car (
                            car_id SERIAL PRIMARY KEY,
                            x1 int,
                            x2 int,
                            y1 int,
                            y2 int,
                            type varchar,
                            fk_image_id integer REFERENCES images (image_id)

                        );
                        ALTER TABLE IF EXISTS car_bbox
                            OWNER to plate_detection_user;

                        CREATE TABLE license_plate (
                            lp_id SERIAL PRIMARY KEY,
                            x1 int,
                            x2 int,
                            y1 int,
                            y2 int,
                            text varchar,
                            type varchar,
                            fk_car_id integer REFERENCES car (car_id)

                        );
                        ALTER TABLE IF EXISTS license_plate
                            OWNER to plate_detection_user
                    """
