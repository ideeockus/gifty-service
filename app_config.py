import os

db_url = os.getenv("DB_URL")
admin_password = os.getenv("ADMIN_PASSWORD")
upload_dir = os.getenv("UPLOAD_DIR", "static/pictures")

orders_comment_max_length = 300

if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)
