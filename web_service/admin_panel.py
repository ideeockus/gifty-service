from flask import request, abort, redirect, Blueprint, current_app, url_for, render_template, jsonify
from typing import Optional
from app_config import admin_password, upload_dir
from werkzeug.utils import secure_filename
from models import GoodsItem, GoodsCategory
from utils.goods_xlx_importer import import_goods_from_xlx
from error_handlers import RequestFailed
from functools import wraps

import os
import io
import db
import models.api


admin_panel = Blueprint("admin", __name__, url_prefix="/admin", template_folder="../templates")


def is_image_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1] in {"png", "jpg", "jpeg"}


def is_authorized(auth_token: Optional[str]) -> bool:
    if auth_token is not None:
        token_is_valid = db.validate_authorization(auth_token)
        if token_is_valid:
            current_app.logger.debug("User authorized")
            return True
    return False


def check_authorized(func):
    @wraps(func)
    def decor(*args, **kwargs):
        request_headers = request.headers  # auth_token должен быть в headers
        print(request_headers)
        if request_headers is None:
            current_app.logger.debug("No data in request")
            return redirect(url_for("admin.signin"))
        else:
            req = models.api.AuthTokenHeader(**request_headers)
            if not is_authorized(req.auth_token):
                return redirect(url_for("admin.signin"))
        return func()
    return decor


@admin_panel.get("/")
@check_authorized
def root():
    # req = models.api.AuthTokenHeader(**request.json)
    return redirect(url_for("admin.panel"))
        # if is_authorized(req.auth_token) else redirect(url_for("admin.signin"))


@admin_panel.get("/panel")
@check_authorized
def panel():
    # req = models.api.AuthTokenHeader(**request.json)
    # if not is_authorized(req.auth_token):
    #     return redirect(url_for("admin.signin"))
    return render_template("admin/panel.html")


# @admin_panel.route("/signin", methods=["GET", "POST"])
# @validate()
# def signin():
#     if is_authorized():
#         return redirect(url_for("admin.panel"))
#
#     if request.method == "GET":
#         return render_template("admin/signin.html")
#     if request.method == "POST":
#         password_is_ok = request.form.get("password") == admin_password
#         if not password_is_ok:
#             current_app.logger.info("admin authorization failed")
#             abort(401)  # unauthorized error
#         auth_token = db.gen_new_auth_token()
#         # if auth_token is None:
#         #     current_app.logger.info("admin authorization failed")
#         #     abort(401)  # unauthorized error
#         session['auth_token'] = auth_token
#         current_app.logger.info("admin authorized")
#         return redirect(url_for("admin.panel"))  # add admin panel later


@admin_panel.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("admin/signin.html")
    if request.method == "POST":
        req = models.api.AdminSignInRequest(**request.json)
        if is_authorized(request.headers.get("Auth-Token")):
            return redirect(url_for("admin.panel"))

        password_is_ok = req.password == admin_password
        if not password_is_ok:
            current_app.logger.info("admin authorization failed")
            return jsonify(models.api.AdminSignInResponse(
                status=models.api.ResponseStatus.Failed
            )), 401
            # abort(401)  # unauthorized error
        auth_token = db.gen_new_auth_token()
        # current_app.logger.info("admin authorized")
        return jsonify(models.api.AdminSignInResponse(
            auth_token=auth_token,
            status=models.api.ResponseStatus.Ok
        ))
        # return redirect(url_for("admin.panel"))  # add admin panel later


@admin_panel.post("/upload_picture")
@check_authorized
def upload_picture():
    print("Uploading file")
    print(request.files)
    # req = models.api.AuthTokenHeader(**request.json)
    # req = request.form
    # req.auth_token = req['auth_token']  # пока все в форме будет, потом надо будет файл нормально отправлять
    #
    # if not is_authorized(req.auth_token):
    #     return redirect(url_for("admin.signin"))
    if 'picture' not in request.files:
        raise RequestFailed
    file = request.files['picture']
    if not file:
        raise RequestFailed
    if not is_image_file(file.filename):
        raise RequestFailed

    filename = secure_filename(file.filename)
    img_path = os.path.join(upload_dir, filename)
    file.save(os.path.join(upload_dir, filename))

    # return {"img_path": filename}, 201
    return jsonify(models.api.UploadPictureResponse(
        img_path=img_path,
        status=models.api.ResponseStatus.Ok
    ))


@admin_panel.post("/add_goods_item")
@check_authorized
def add_goods_item():
    req = models.api.AddGoodsItemRequest(**request.json)

    # if not is_authorized(req.auth_token):
    #     return redirect(url_for("admin.signin"))
    # name = request.json.get("name")
    # description = request.json.get("description")
    # price = request.json.get("price")
    # img_path = request.json.get("img_path")
    # category = request.json.get("category")
    #
    # if not isinstance(price, float) and not isinstance(price, int):
    #     abort(400, "price must me float value")
    # if category not in [category_code for category_code in GoodsCategory]:
    #     abort(400, f"category {category} not exist")
    # category = GoodsCategory(category)

    item = GoodsItem(name=req.name, description=req.description,
                     price=req.price, img_path=req.img_path, category=req.category)

    item_id = db.add_goods_item(item)
    # return {"item_id": item_id}
    return jsonify(models.api.AddGoodsItemResponse(
        item_id=item_id,
        status=models.api.ResponseStatus.Ok
    ))


@admin_panel.post("/edit_goods_item")
@check_authorized
def edit_goods_item():
    req = models.api.EditGoodsItemRequest(**request.json)

    # if not is_authorized(req.auth_token):
    #     return redirect(url_for("admin.signin"))
    # item_id = request.json.get("id")
    # name = request.json.get("name")
    # description = request.json.get("description")
    # price = request.json.get("price")
    # img_path = request.json.get("img_path")
    # category = request.json.get("category")

    # print(item_id, name, description, price, img_path, category)

    # if not isinstance(item_id, int):
    #     current_app.logger.warning("Goods Item ID not provided")
    #     abort(400, "Goods Item ID not provided")
    # if not isinstance(price, float) and not isinstance(price, int):
    #     abort(400, "price must me float value")
    # if category not in [category_code for category_code in GoodsCategory]:
    #     abort(400, f"category {category} not exist")
    # category = GoodsCategory(category)

    item = GoodsItem(id=req.item_id, name=req.name, description=req.description,
                     price=req.price, img_path=req.img_path, category=req.category)

    status = db.edit_goods_item(item)

    return jsonify(models.api.CommonResponse(
        status=models.api.ResponseStatus.Ok if status else models.api.ResponseStatus.Failed
    ))
    # return {"status": status}


@admin_panel.post("/remove_goods_item")
@check_authorized
def remove_goods_item():
    req = models.api.RemoveGoodsItemRequest(**request.json)
    # item_id = request.json.get("id")

    # if not isinstance(item_id, int):
    #     current_app.logger.warning("Goods Item ID not provided")
    #     abort(400, "Goods Item ID not provided")

    status = db.del_goods_item_by_id(req.item_id)

    return jsonify(models.api.CommonResponse(
        status=models.api.ResponseStatus.Ok if status else models.api.ResponseStatus.Failed
    ))


@admin_panel.post("/import_xlx_goods")
@check_authorized
def import_xlx_goods():
    if 'goods_xlx' not in request.files:
        abort(400, "no file attached")
    goods_xlx = request.files['goods_xlx']
    goods_xlx_in_memory = io.BytesIO()
    goods_xlx.save(goods_xlx_in_memory)  # выгрузка в память

    filename = secure_filename(goods_xlx.filename)
    import_goods_from_xlx(goods_xlx_in_memory)

    return {"status": True}, 201
