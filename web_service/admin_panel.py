from flask import request, abort, redirect, Blueprint, current_app, url_for, render_template, jsonify
from typing import Optional
from app_config import admin_password, upload_dir
from werkzeug.utils import secure_filename
from utils.goods_xlx_importer import import_goods_from_xlx
from error_handlers import RequestFailed
from functools import wraps
from models import GoodsItem, GoodsCategory, BoxType
from models import api

import os
import io
import db


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
        if request_headers is None:
            current_app.logger.debug("No data in request")
            return redirect(url_for("admin.signin"))
        else:
            req = api.AuthTokenHeader(**request_headers)
            if not is_authorized(req.auth_token):
                return redirect(url_for("admin.signin"))
        return func()
    return decor


@admin_panel.get("/")
@check_authorized
def root():
    return redirect(url_for("admin.panel"))


@admin_panel.get("/panel")
@check_authorized
def panel():
    return render_template("admin/panel.html")


@admin_panel.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("admin/signin.html")
    if request.method == "POST":
        req = api.AdminSignInRequest(**request.json)
        if is_authorized(request.headers.get("Auth-Token")):
            return redirect(url_for("admin.panel"))

        password_is_ok = req.password == admin_password
        if not password_is_ok:
            current_app.logger.info("admin authorization failed")
            return jsonify(api.AdminSignInResponse(
                status=api.ResponseStatus.Failed
            )), 401
        auth_token = db.gen_new_auth_token()
        return jsonify(api.AdminSignInResponse(
            auth_token=auth_token,
            status=api.ResponseStatus.Ok
        ))


@admin_panel.post("/upload_picture")
@check_authorized
def upload_picture():
    print("Uploading file")
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

    return jsonify(api.UploadPictureResponse(
        img_path=img_path,
        status=api.ResponseStatus.Ok
    ))


@admin_panel.post("/add_goods_item")
@check_authorized
def add_goods_item():
    req = api.AddGoodsItemRequest(**request.json)

    item = GoodsItem(name=req.name, description=req.description,
                     price=req.price, img_path=req.img_path, category=req.category)

    item_id = db.add_goods_item(item)
    return jsonify(api.AddGoodsItemResponse(
        item_id=item_id,
        status=api.ResponseStatus.Ok
    ))


@admin_panel.post("/edit_goods_item")
@check_authorized
def edit_goods_item():
    # TODO: доделать метод чтобы можно было переавать не все значения (реадктировать поля выборочно)
    req = api.EditGoodsItemRequest(**request.json)

    item = GoodsItem(id=req.item_id, name=req.name, description=req.description,
                     price=req.price, img_path=req.img_path, category=req.category)

    status = db.edit_goods_item(item)

    return jsonify(api.CommonResponse(
        status=api.ResponseStatus.Ok if status else api.ResponseStatus.Failed
    ))


@admin_panel.post("/remove_goods_item")
@check_authorized
def remove_goods_item():
    req = api.RemoveGoodsItemRequest(**request.json)

    status = db.del_goods_item_by_id(req.item_id)

    return jsonify(api.CommonResponse(
        status=api.ResponseStatus.Ok if status else api.ResponseStatus.Failed
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


@admin_panel.post("/set_order_status")
@check_authorized
def set_order_status():
    req = api.SetOrderStatusRequest(**request.json)

    status = db.set_order_status_by_id(req.order_id, req.order_status)

    return jsonify(api.CommonResponse(
        status=api.ResponseStatus.Ok if status else api.ResponseStatus.Failed
    ))
