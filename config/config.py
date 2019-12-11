import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class Config(object):
    """Common configurations
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class DevelopmentConfig(Config):
    """Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configurations
    """

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configurations
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    #SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER='C:\\flask-school-app-and-api-master\\app\\export'
    JOBS=[{
        "id":"job1",
        "func":"app:WarnPrices",
        "args":"",
        "trigger":{
            "type":"interval",
            "days":1
        }
    }]
    SESSION_PROTECTION="strong"



class CeleryConfig:
    BROKER_URL="redis://:1qaz@WSX@172.18.1.101:6379/0"
    CELERY_RESULT_BACKEND="redis://:1qaz@WSX@172.18.1.101:6379/1"

    CELERY_TASK_RESULT_EXPIRES = 60 #后端任务执行超时时间


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
