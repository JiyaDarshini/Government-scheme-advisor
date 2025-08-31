import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://app:secret@db:5432/schemesdb')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
