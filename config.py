from pathlib import Path

basedir = Path(__file__).parent.parent

class BaseConfig:
    SECRET_KEY = "3AzyT0523ZaQjYdo16b"
    WTF_CSRF_SECRET_KEY = "AmaskfqljkewQEFQWFAFKDSl1"
    UPLOAD_FOLDER = str(Path(basedir, "apps", "book/static/images/thumnail"))
    SESSION_TYPE = 'filesystem'

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3306/minibook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3306/minibook'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config = {
    "testing" : TestingConfig,
    "local" : LocalConfig
}