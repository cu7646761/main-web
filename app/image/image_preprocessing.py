from PIL import Image
from io import BytesIO
import PIL

IMAGE_THUMBNAIL_SIZE = 120, 120


def resize(origin_image, base_width=600):
    # resize image with max width given

    img = Image.open(BytesIO(origin_image.read()))

    wpercent = (base_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))

    img_resized = img.resize((base_width, hsize), PIL.Image.ANTIALIAS)

    return img_resized


def make_thumbnail(origin_image):
    # make a thumbnail with 120x120px
    img = Image.open(BytesIO(origin_image.read()))
    img.thumbnail(IMAGE_THUMBNAIL_SIZE)
    return img


def compress(origin_image):
    return ""
