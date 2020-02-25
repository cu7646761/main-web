import enum


class Pages(enum.IntEnum):
    NUMBER_PER_PAGE = 10
    VISIBLE_PAGE = 6


class Errors(enum.Flag):
    ERROR_NONE = "Error: all fields is not completed"
    ERROR_EXIST = "Error: this fields is exist"


SERVER_NAME = "http://127.0.0.1:5000"
# SERVER_NAME = "https://blog-an-uong.herokuapp.com"
