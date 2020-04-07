import enum
import os
from dotenv import load_dotenv


_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

API_KEY = os.getenv('API_KEY', "")

class Pages(enum.IntEnum):
    NUMBER_PER_PAGE = 10
    VISIBLE_PAGE = 6


class Errors(enum.Flag):
    ERROR_NONE = "Error: all fields is not completed"
    ERROR_EXIST = "Error: this fields is exist"


SERVER_NAME = "http://127.0.0.1:5000"
LINK_IMG = SERVER_NAME + "/static/images/"
LINK_IMG_AVATAR_DEF = os.path.join(LINK_IMG, 'avatar_an_danh.jpg')
ADMIN_MAIL = "vuongsponges@gmail.com"
# SERVER_NAME = "https://blog-an-uong.herokuapp.com"

GENDER = {"Name": 0, "Nữ": 1, "Khác": 2}

# upload file
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

CLASS_LIST = {
    1: 'SS', 2: 'SS', 3: 'S', 4: 'S',
    5: 'A', 6: 'A', 7: 'A', 8: 'A',
    9: 'B', 10: 'B', 11: 'B', 12: 'B',
    13: 'C', 14: 'C', 15: 'C', 16: 'C',
    17: 'D', 18: 'D', 19: 'D', 20: 'D',
    21: 'E', 22: 'E', 23: 'E', 24: 'E',
    25: 'F', 26: 'F', 27: 'F', 28: 'F'
}

FILTER_LIST = {
    1: 'SS+', 2: 'SS', 3: 'S+', 4: 'S',
    5: 'AA+', 6: 'AA', 7: 'A+', 8: 'A',
    9: 'BB+', 10: 'BB', 11: 'B+', 12: 'B',
    13: 'CC+', 14: 'CC', 15: 'C+', 16: 'C',
    17: 'DD+', 18: 'DD', 19: 'D+', 20: 'D',
    21: 'EE+', 22: 'EE', 23: 'E+', 24: 'E',
    25: 'FF+', 26: 'FF', 27: 'F+', 28: 'F'
}

PRED_LIST = {
    'SS+': 1,'SS': 2,'S+': 3,'S': 4,
    'AA+': 5,'AA': 6,'A+': 7,'A': 8,
    'BB+': 9,'BB': 10,'B+': 11,'B': 12,
    'CC+': 13,'CC': 14,'C+': 15,'C': 16,
    'DD+': 17,'DD': 18,'D+': 19,'D': 20,
    'EE+': 21,'EE': 22,'E+': 23,'E': 24,
    'FF+': 25,'FF': 26,'F+': 27,'F': 28
}