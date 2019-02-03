from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

from app.main.config import Config
from app.main.service.audio_source.vk_provider import VkProvider
from app.main.service.celery_service import make_celery
from app.main.service.file_service import FileService

flask_bcrypt = Bcrypt()
vk_audio = VkProvider()
file_service = FileService()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(Config)

db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

flask_bcrypt.init_app(app)
celery = make_celery(app)

vk_audio.init_app(app.config['VK_LOGIN'], app.config['VK_PASSWORD'])
file_service.init_app(url=app.config['S3_URL'],
                      client_id=app.config['S3_CLIENT_ID'],
                      secret_key=app.config['S3_SECRET_KEY'],
                      region=app.config['S3_REGION'],
                      bucket_name=app.config['S3_BUCKET_NAME'])

from app.main.service.stream_service import StreamService

stream_service = StreamService()

from app.main.service import background_task_service, user_service
