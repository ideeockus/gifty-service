from typing import Optional
from flask import request, abort, session, redirect, Blueprint, current_app, url_for, render_template

import db
from app_config import admin_password, upload_dir
from werkzeug.utils import secure_filename

import utils
import os

from models import GoodsItem, GoodsCategory

admin_panel = Blueprint("admin", __name__, url_prefix="/admin")


# def authorize_admin(password: str) -> Optional[str]:
#     if password == admin_password:
#         return utils.gen_auth_token()


def is_image_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1] in {"png", "jpg", "jpeg"}


def is_authorized() -> bool:
    if "auth_token" in session:
        auth_token = session.get("auth_token")
        token_is_valid = db.validate_authorization(auth_token)
        if token_is_valid:
            current_app.logger.debug("User authorized")
            return True
    return False


@admin_panel.get("/")
def root():
    # if "auth_token" in session:
    #     auth_token = session.get("auth_token")
    #     token_is_valid = db.validate_authorization(auth_token)
    #     if token_is_valid:
    #         return redirect(url_for("admin.panel"))
    # return redirect(url_for("admin.signin"))
    return redirect(url_for("admin.panel")) if is_authorized() else redirect(url_for("admin.signin"))


@admin_panel.get("/panel")
def panel():
    if not is_authorized():
        return redirect(url_for("admin.signin"))
    return render_template("admin/panel.html")


@admin_panel.route("/signin", methods=["GET", "POST"])
def signin():
    if is_authorized():
        return redirect(url_for("admin.panel"))

    if request.method == "GET":
        return render_template("admin/signin.html")
    if request.method == "POST":
        password_is_ok = request.form.get("password") == admin_password
        auth_token = db.gen_new_auth_token()
        if auth_token is None:
            current_app.logger.info("admin authorization failed")
            abort(401)  # unauthorized error
        session['auth_token'] = auth_token
        current_app.logger.info("admin authorized")
        return redirect(url_for("admin.panel"))  # add admin panel later


# @admin_panel.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     current_app.logger.debug(f"form: {request.form}")
#     current_app.logger.debug(f"files: {request.files}")
#     current_app.logger.debug(f"json: {request.json}")
#     # for file in request.files:
#     #     file.save(f"{upload_dir}{secure_filename(file.filename)}")
#     if 'file' not in request.files:
#         return redirect(request.url)
#     file = request.files['file']
#     if file and is_image_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(upload_dir, filename))
#         return "File uploaded"
#     return "An error occurred"


@admin_panel.post("/upload_picture")
def upload_picture():
    # current_app.logger.debug(f"form: {request.form}")
    # current_app.logger.debug(f"files: {request.files}")
    # current_app.logger.debug(f"json: {request.json}")
    # current_app.logger.debug(f"data: {request.data}")
    if 'picture' not in request.files:
        abort(400, "no file attached")
    file = request.files['picture']
    if not file:
        abort(400, "No picture in request")
    if not is_image_file(file.filename):
        abort(400, "only pictures allowed")

    filename = secure_filename(file.filename)
    img_path = os.path.join(upload_dir, filename)

    # if file and is_image_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(upload_dir, filename))
    file.save(os.path.join(upload_dir, filename))

    return {"img_path": filename}, 201

# @admin_panel.post("/upload_picture/<filename>")
# def upload_picture(filename):
#     current_app.logger.debug(f"form: {request.form}")
#     current_app.logger.debug(f"files: {request.files}")
#     current_app.logger.debug(f"json: {request.json}")
#     current_app.logger.debug(f"data: {request.data}")
#     if "/" in filename:
#         abort(400, "no subdirectories allowed")
#     if not is_image_file(filename):
#         abort(400, "only pictures allowed")
#
#     img_path = os.path.join(upload_dir, secure_filename(filename))
#     with open(img_path, "wb") as fp:
#         fp.write(request.data)
#
#     return img_path, 201


@admin_panel.post("/add_goods_item")
def add_goods_item():
    # item_id = request.json.get("id")
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    img_path = request.json.get("img_path")
    category = request.json.get("category")

    if not isinstance(price, float) and not isinstance(price, int):
        abort(400, "price must me float value")
    if category not in [category_code for category_code in GoodsCategory]:
        abort(400, f"category {category} not exist")
    category = GoodsCategory(category)

    item = GoodsItem(name=name, description=description, price=price, img_path=img_path, category=category)

    item_id = db.add_goods_item(item)
    return {"item_id": item_id}


@admin_panel.post("/edit_goods_item")
def edit_goods_item():
    item_id = request.json.get("id")
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    img_path = request.json.get("img_path")
    category = request.json.get("category")

    print(item_id, name, description, price, img_path, category)

    if not isinstance(item_id, int):
        current_app.logger.warning("Goods Item ID not provided")
        abort(400, "Goods Item ID not provided")
    if not isinstance(price, float) and not isinstance(price, int):
        abort(400, "price must me float value")
    if category not in [category_code for category_code in GoodsCategory]:
        abort(400, f"category {category} not exist")
    category = GoodsCategory(category)

    item = GoodsItem(id=item_id, name=name, description=description, price=price, img_path=img_path, category=category)

    db.edit_goods_item(item)

    return {"status": True}
