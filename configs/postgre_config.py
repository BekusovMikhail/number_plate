posgres_DB = "plate_detection_db"
posgres_user = "plate_detection_user"
posgres_user_password = "lprpassword"
sql_alchemy_engine = f"postgresql+psycopg2://{posgres_user}:{posgres_user_password}@127.0.0.1/{posgres_DB}"
