from flask import Blueprint, jsonify
from pydantic import ValidationError
import models.api

error_handler = Blueprint("error_handler", __name__)


class RequestFailed(Exception):
    def __repr__(self):
        return "Request Failed"


@error_handler.app_errorhandler(404)
def page_not_found(error):
    return "Error 404 Not Found"


@error_handler.app_errorhandler(RequestFailed)
def page_not_found(error):
    return jsonify(models.api.CommonResponse(
        status=models.api.ResponseStatus.Failed
    ))


@error_handler.app_errorhandler(ValidationError)
def page_not_found(error: ValidationError):
    return jsonify(
        error.errors()
    )
