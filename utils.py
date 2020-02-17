from flask import json
from app import bcrypt


class Utils:
    @staticmethod
    def hash_password(str_psw):
        if str_psw is None:
            return None
        str_psw = bcrypt.generate_password_hash(str_psw)
        return str_psw

    @staticmethod
    def check_password(psw_1, psw_2):
        # psw_1: pass that you try to login
        # psw_2: pass that you save in db
        if bcrypt.check_password_hash(psw_2, psw_1):
            return True
        return False

    @staticmethod
    def decode_json(payload):
        return json.loads(payload.decode('utf-8'))

    @staticmethod
    def print_json(payload):
        return json.dumps(payload, indent=4, sort_keys=True)
