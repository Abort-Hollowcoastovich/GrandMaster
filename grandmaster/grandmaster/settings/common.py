import environ
from pathlib import Path

env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
