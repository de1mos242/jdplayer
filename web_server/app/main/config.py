import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jdplayer_secret_key')

    VK_LOGIN = os.getenv("VK_LOGIN", 'vk_login_not_set')
    VK_PASSWORD = os.getenv("VK_PASSWORD", 'vk_password_not_set')

    S3_URL = os.getenv("S3_URL", "http://localhost:9001")
    S3_CLIENT_ID = os.getenv("S3_CLIENT_ID", "minio")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "minio123")
    S3_REGION = os.getenv("S3_REGION", "us-east-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", 'jdplayer')

    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'amqp://admin:mypass@localhost:5673//')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://admin:mypass@localhost:5673//')

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", 'sqlite:///' + os.path.join(basedir, 'flask_jdplayer_main.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)

    DEBUG = os.getenv("DEBUG", True)


key = Config.SECRET_KEY
