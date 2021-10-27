import os

db_url = os.getenv("DB_URL")
admin_password = os.getenv("ADMIN_PASSWORD")
upload_dir = os.getenv("UPLOAD_DIR", "static/pictures")

if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)
