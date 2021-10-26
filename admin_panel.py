from typing import Optional
from flask import request, abort, session, redirect, Blueprint, current_app, url_for, render_template
from app_config import admin_password, upload_dir
from werkzeug.utils import secure_filename

import utils
import os


admin_panel = Blueprint("admin", __name__, url_prefix="/admin")


def authorize_admin(password: str) -> Optional[str]:
    if password == admin_password:
        return utils.gen_auth_token()


def is_image_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1] in {"png", "jpg", "jpeg"}


@admin_panel.get("/panel")
def panel():
    return render_template("admin/panel.html")


@admin_panel.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        # return url_for("static", filename="pages/signin.html")
        return render_template("admin/signin.html")
    if request.method == "POST":
        if "auth_token" in session:
            pass  # check if token is valid
        password = request.form.get("password")
        auth_token = authorize_admin(password)
        if auth_token is None:
            current_app.logger.info("admin authorization failed")
            abort(401)  # unauthorized error
        session['auth_token'] = auth_token
        current_app.logger.info("admin authorized")
        return redirect(url_for("admin.panel"))  # add admin panel later


@admin_panel.route("/upload", methods=["GET", "POST"])
def upload_file():
    current_app.logger.debug(f"files: {request.files}")
    # for file in request.files:
    #     file.save(f"{upload_dir}{secure_filename(file.filename)}")
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and is_image_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_dir, filename))
        return "File uploaded"
    return "An error occurred"


@admin_panel.post("/edit_item")
def edit_goods_item():
    item_id = request.form.get("id")
    if not item_id.isalnum():
        current_app.logger.warning("Goods Item ID not provided")
        return "Goods Item ID not provided"
    item_id = int(item_id)

    current_app.logger.warning(f"{request.get_data()}")
    current_app.logger.warning(f"{request.get_json()}")

    name = request.form.get("name")
    description = request.form.get("description")
    cost = request.form.get("cost")
    img_path = request.form.get("img_path")
    category = request.form.get("category")
