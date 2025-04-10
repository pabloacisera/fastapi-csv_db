from dotenv import dotenv_values

config = dotenv_values('.env')

sqlite_uri = config.get('SQLITE_URI')
SECRET_KEY = config.get('SECRET_KEY')
ALGORITHM = config.get('ALGORITHM')
ACCESS_TOKEN_EXPIRES = config.get('ACCESS_TOKEN_EXPIRES')
