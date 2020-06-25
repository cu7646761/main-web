import enum
import os
from dotenv import load_dotenv


_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

API_KEY = os.getenv('API_KEY', "AIzaSyBFIs_p577J18Oqokx2EdZZVVk9XLLzk6Q")

class Pages(enum.IntEnum):
    NUMBER_PER_PAGE = 10
    VISIBLE_PAGE = 6


class Errors(enum.Flag):
    ERROR_NONE = "Error: all fields is not completed"
    ERROR_EXIST = "Error: this fields is exist"


SERVER_NAME = "http://localhost:5000"
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

PRED_LIST2 = {
    'SS': (0,1000),'S': (1000,500),
    'A': (500, 200),
    'B': (200, 100),
    'C': (100, 50),
    'D': (50, 10),
    'E': (10, 3),
    'F': (3, 0)
}

CATE_LIST = {
    'japanese': 'Món Nhật',
    'korean': 'Món Hàn',
    'seafood': 'Hải sản',
    'fastfood': 'Fastfood',
    'vegetarian': 'Món chay',
    'cafe': 'Quán cà phê, giải khát',
    'smoothie': 'Sinh tố',
    'cake': 'Các loại bánh',
    'drinking': 'Quán nhậu',
    'meat-beaf': 'Thịt heo, thịt bò',
    'chicken': 'Gà',
    'water-dish': 'Món nước, bún, phở',
    'bar-club': 'Bar, club',
}

POS_DICT = {
    'good':3, 'best':3, 'yummy':3, 'clean':1, 'nice':3, 'beautiful':4, 'ok':1, 'oke':1, 'love':1, 'like':1,
    'polite':1, 'awesome':1, 'happy':1, 'great':1, 'perfect':1, 'delicious':3, 'well':1, 'cool':1, 'appreciate':1,
    'cozy':1, 'lovely':1, ' reasonably':1, 'cheap':1, 'fast':1 ,'tasty':1, 'affordable':1, 'attractive':1, 'cute':1,
    'pretty':3, "vibe":1, "dedicated":1, 'quiet':1, 'convenient':1, 'exciting':1, 'excited':1, 'amazing':1, 'enjoy':1,
    'enjoyed':1, 'pleasure':1, 'pleased':1, 'friendly':1, 'quick':1, 'satisfied':1, 'wonderfull':1, 'okay':1, 
    'enthusiastic':1, 'loved':1, 'highly':1, 'impress':1 ,'impressed':1, 'impression':1, 'liked':1, 'appreciate':1, 'special':1,
    'lively':1, 'excellent':3, 'wonderful':1
}
BAD_DICT = {
    'bad':1, 'worst':1, 'disgusting':1, 'dirty':1, 'ugly':1, 'hate':1, 'impolite':1, 'sad':1, 'disappointed':1, 'dislike':1,
    'poor':1, 'noisy':1, 'expensive':1, 'fuck':3, 'fucking':3, 'lousy':2, 'slow':1, 'slowly':1, 'small':1, 'lack':1, 'weak':1,
    'broken':1, 'disregard':1, 'wasted':1, 'boring':1, 'horrible':1, 'angry':1, 'careless':1, 'failed':1, 'dissatisfied':1,
    'chemicals':1 , 'chemical':1, 'unsafe':1, 'unloading':1, 'suck':1, 'shit':1, 'hated':1, 'abhor':1, 'abominable':1, 'confuse':1,
    'confusion':1, 'embarrassed':1, 'nervous':1, 'terible':1, 'horror':1, 'horrible':1, 'horribly':1, 'terrified':1
}
NEG_WORDS = {
    'no':1, 'not':1, 'nerver':1, "won't":1, "aren't":1, "don't":1, "isn't":1, "doesn't":1, "can't":1, "couldn't":1, 'none':1,
    "haven't":1, "hasn't":1, "didn't":1, "wasn't":1, "weren't":1, "wouldn't":1, 'hardly':1, 'k':1, 'ko':1, 'never':1
}
TEMP_DICT = {
    'simple':1, 'normal':1, 'temporary':1, 'ordinary':1, 'dc':1, 'tam':1, 'normally':1, 'average':1 
}
NEUTRAL_WORDS = {
    'staff':3, 'staffs':3, 'i':1, 'me':1,
    'food':3, 'foods':3, 'place':3, 'places':3, 'service':3,
    'service':1, 'services':1, 'restaurant':1, 'restaurants':1, 'space':1, 'spaces':1,
    'atmosphere':1, 'price':1, 'prices':1, 'taste':1, 'table':1, 'shop':1, 'seat':1,
    'seats':1, 'family':1, 'meal':1, 'people':1, 'meals':1, 'dinner':1, 'view':1, 'design':1,
    'friend':1, 'friends':1, 'customer':1, 'customers':1, 'waiter':1, 'waitress':1, 'dish':1, 'dishes':1,
    'time':1, 'times':1, 'quality':1, 'location':1, 'decoration':1, 'lunch':1, 'style':1, 'town':1, 'experience':1,
    'floor':1, 'cuisine':1, 'center':1, 'everything':1, 'air':1, 'money':1, 'one':1, 'some':1, 'more':1, 'choice':1
}