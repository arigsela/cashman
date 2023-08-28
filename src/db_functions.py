import os, json
from src.aws_functions import fetch_secrets_from_aws

def get_db_settings():
    # Getting environment variables
    db_dialect = os.environ.get("DB_DIALECT")
    db_url = os.environ.get("DB_DATABASE_URL")
    db_name = os.environ.get("DB_DATABASE_NAME")
    db_credentials_secret = os.environ.get("DB_CREDENTIALS_SECRET")
    db_secretkey = os.environ.get("DB_SECRET_KEY")

    # Retrieving mysql database credentials from AWS
    db_credentials = json.loads(fetch_secrets_from_aws(db_credentials_secret))

    # Setting SQLALCHEMY connection string
    db_uri = "{}://{}:{}@{}/{}".format(db_dialect, db_credentials.get('username'), db_credentials.get('password'), db_url, db_name )

    return db_uri, db_secretkey