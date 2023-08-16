# configuration
class Config:
    DEBUG = True
    # db
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:root@localhost:5432/Melonoma_Cancer'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
