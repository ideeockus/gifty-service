import secrets


def gen_auth_token() -> str:
    token = secrets.token_urlsafe(20)
    return token
