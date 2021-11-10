import os

db_url = os.getenv("DB_URL")
admin_password = os.getenv("ADMIN_PASSWORD")
upload_dir = os.getenv("UPLOAD_DIR", "static/pictures")

# ------ web service confs --------
orders_comment_max_length = 300
default_image_path = "static/pictures/no_image.png"

if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)
